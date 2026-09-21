//! The C++-ABI bridge: object layout and hand-laid vtables.
//!
//! VirtualDJ calls the *plugin* through a real Itanium-ABI C++ vtable, and
//! writes some of the plugin object's **data members directly** (`hInstance`,
//! `cb`, and the DSP subclass fields) — there are no setter virtuals. So both
//! the vtable slot order and the field offsets here are load-bearing. Every
//! one of them is checked against the real SDK headers, compiled by the real
//! compiler, in `tests/layout.rs`.
//!
//! Layout facts encoded here (macOS, Itanium C++ ABI):
//!
//! - Vtable slots are in declaration order. `IVdjPlugin8`'s virtual destructor
//!   occupies **two** consecutive slots (complete D1, then deleting D0), which
//!   is why `OnParameter` is slot 5, not 4.
//! - A vtable is preceded by an offset-to-top word and a typeinfo pointer; the
//!   object's vptr points *past* them at slot 0. We emit a null typeinfo —
//!   safe unless the host runs `dynamic_cast`/`typeid` on plugin pointers,
//!   which the live loading evidence (type negotiation by IID, not RTTI)
//!   gives no sign of.
//! - `VDJ_API` is empty on macOS, so virtual calls are plain C calls with
//!   `this` first. On arm64, constructors/destructors return `this`; our
//!   destructor shims return the pointer, which x86_64 callers simply ignore.

use crate::host::Host;
use crate::sys::*;
use crate::{DspContext, DspPlugin, PluginInfo, VdjPlugin};
use std::ffi::{c_char, c_void, CString};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::ptr;

// ---------------------------------------------------------------------------
// Vtable slot tables
// ---------------------------------------------------------------------------

/// Slots of `IVdjPlugin8` in vtable order.
#[repr(C)]
pub struct BasicSlots {
    pub on_load: unsafe extern "C" fn(this: *mut c_void) -> HRESULT,
    pub on_get_plugin_info:
        unsafe extern "C" fn(this: *mut c_void, info: *mut TVdjPluginInfo8) -> HRESULT,
    pub release: unsafe extern "C" fn(this: *mut c_void) -> u32,
    /// D1: destroy in place, no deallocation.
    pub dtor_complete: unsafe extern "C" fn(this: *mut c_void) -> *mut c_void,
    /// D0: destroy and deallocate (`delete this`).
    pub dtor_deleting: unsafe extern "C" fn(this: *mut c_void) -> *mut c_void,
    pub on_parameter: unsafe extern "C" fn(this: *mut c_void, id: i32) -> HRESULT,
    pub on_get_parameter_string: unsafe extern "C" fn(
        this: *mut c_void,
        id: i32,
        out_param: *mut c_char,
        out_param_size: i32,
    ) -> HRESULT,
    pub on_get_user_interface:
        unsafe extern "C" fn(this: *mut c_void, iface: *mut TVdjPluginInterface8) -> HRESULT,
}

/// Slots of `IVdjPluginDsp8`: the base slots, then its own in declaration order.
#[repr(C)]
pub struct DspSlots {
    pub base: BasicSlots,
    pub on_start: unsafe extern "C" fn(this: *mut c_void) -> HRESULT,
    pub on_stop: unsafe extern "C" fn(this: *mut c_void) -> HRESULT,
    pub on_process_samples:
        unsafe extern "C" fn(this: *mut c_void, buffer: *mut f32, nb: i32) -> HRESULT,
}

/// A vtable as the ABI lays it out: preamble, then the slots. The object's
/// vptr points at `.slots`, not at the struct start.
#[repr(C)]
pub struct VtblStorage<V> {
    offset_to_top: isize,
    typeinfo: *const c_void,
    pub slots: V,
}

// ---------------------------------------------------------------------------
// Host-written data members
// ---------------------------------------------------------------------------

/// `IVdjPlugin8` has no subclass fields beyond the shared prefix.
#[repr(C)]
#[derive(Default)]
pub struct NoFields;

/// `IVdjPluginDsp8`'s host-written members, in declaration order after `cb`.
///
/// Caveat from live testing (`docs/VDJScript Local Test Tracker.md`,
/// 2026-08-15): `song_bpm` is *samples between beats*, and reads as a 120 BPM
/// default (22050 @ 44.1 kHz) while the deck is idle — it is not always the
/// loaded track's tempo.
#[repr(C)]
#[derive(Default, Clone, Copy)]
pub struct DspFields {
    pub sample_rate: i32,
    pub song_bpm: i32,
    pub song_pos_beats: f64,
}

// ---------------------------------------------------------------------------
// The instance
// ---------------------------------------------------------------------------

/// One live plugin object. The prefix (`vptr` … `host_fields`) is exactly the
/// C++ object layout the host expects and pokes; everything after is private
/// Rust state the host never sees.
#[repr(C)]
pub struct Instance<V, X, P> {
    vptr: *const c_void,
    /// Written by the host: `CFBundleRef` on macOS.
    hinstance: *mut c_void,
    /// Written by the host before `OnLoad`.
    cb: *mut IVdjCallbacks8,
    /// Subclass members the host writes (empty for a basic plugin).
    host_fields: X,
    // --- host-invisible from here ---
    vtbl: VtblStorage<V>,
    info: Option<InfoStrings>,
    plugin: P,
}

pub type BasicInstance<P> = Instance<BasicSlots, NoFields, P>;
pub type DspInstance<P> = Instance<DspSlots, DspFields, P>;

/// Owned backing storage for the pointers handed out in `OnGetPluginInfo`.
/// Held for the instance's lifetime — the SDK never says when the host stops
/// reading them (same rule the skin-interface buffers were verified to need).
struct InfoStrings {
    name: CString,
    author: CString,
    description: CString,
    version: CString,
    flags: u32,
}

fn cstring_lossy(s: &str) -> CString {
    CString::new(s.replace('\0', " ")).expect("NULs removed")
}

impl InfoStrings {
    fn from_info(info: &PluginInfo) -> InfoStrings {
        InfoStrings {
            name: cstring_lossy(&info.name),
            author: cstring_lossy(&info.author),
            description: cstring_lossy(&info.description),
            version: cstring_lossy(&info.version),
            flags: info.flags,
        }
    }
}

// ---------------------------------------------------------------------------
// Shims
// ---------------------------------------------------------------------------
//
// Every shim: recover the instance, catch_unwind around plugin code, map a
// panic to E_FAIL. A panic must never unwind into VirtualDJ.

unsafe fn inst<'a, V, X, P>(this: *mut c_void) -> &'a mut Instance<V, X, P> {
    &mut *(this as *mut Instance<V, X, P>)
}

unsafe extern "C" fn on_load_shim<V, X, P: VdjPlugin>(this: *mut c_void) -> HRESULT {
    let i = inst::<V, X, P>(this);
    let host = Host::from_cb(i.cb);
    match catch_unwind(AssertUnwindSafe(|| i.plugin.on_load(&host))) {
        Ok(Ok(())) => S_OK,
        Ok(Err(e)) => e.0,
        Err(_) => E_FAIL,
    }
}

unsafe extern "C" fn on_get_plugin_info_shim<V, X, P: VdjPlugin>(
    this: *mut c_void,
    out: *mut TVdjPluginInfo8,
) -> HRESULT {
    if out.is_null() {
        return E_INVALIDARG;
    }
    let i = inst::<V, X, P>(this);
    let built = catch_unwind(AssertUnwindSafe(|| InfoStrings::from_info(&i.plugin.info())));
    let strings = match built {
        Ok(s) => s,
        Err(_) => return E_FAIL,
    };
    i.info = Some(strings);
    let s = i.info.as_ref().expect("just set");
    // Only the base TVdjPluginInfo8 fields are touched. The host may pass the
    // Extension1 struct (it sets VDJFLAG_EXTENSION1 to say so); the extension's
    // mouseCallbacks slot is left alone.
    (*out).plugin_name = s.name.as_ptr();
    (*out).author = s.author.as_ptr();
    (*out).description = s.description.as_ptr();
    (*out).version = s.version.as_ptr();
    (*out).bitmap = ptr::null_mut();
    (*out).flags = s.flags;
    S_OK
}

unsafe extern "C" fn release_shim<V, X, P>(this: *mut c_void) -> u32 {
    drop(Box::from_raw(this as *mut Instance<V, X, P>));
    S_OK as u32
}

/// D1 — destroy without deallocating. The host owns neither our allocator nor
/// our memory, so all it can meaningfully do alone is drop the fields; the
/// allocation itself leaks in that (never-observed) path.
unsafe extern "C" fn dtor_complete_shim<V, X, P>(this: *mut c_void) -> *mut c_void {
    ptr::drop_in_place(this as *mut Instance<V, X, P>);
    this
}

/// D0 — `delete this`.
unsafe extern "C" fn dtor_deleting_shim<V, X, P>(this: *mut c_void) -> *mut c_void {
    drop(Box::from_raw(this as *mut Instance<V, X, P>));
    this
}

unsafe extern "C" fn on_parameter_shim<V, X, P: VdjPlugin>(this: *mut c_void, id: i32) -> HRESULT {
    let i = inst::<V, X, P>(this);
    let host = Host::from_cb(i.cb);
    match catch_unwind(AssertUnwindSafe(|| i.plugin.on_parameter(&host, id))) {
        Ok(Ok(())) => S_OK,
        Ok(Err(e)) => e.0,
        Err(_) => E_FAIL,
    }
}

unsafe extern "C" fn on_get_parameter_string_shim<V, X, P: VdjPlugin>(
    this: *mut c_void,
    id: i32,
    out_param: *mut c_char,
    out_param_size: i32,
) -> HRESULT {
    if out_param.is_null() || out_param_size <= 0 {
        return E_INVALIDARG;
    }
    let i = inst::<V, X, P>(this);
    let host = Host::from_cb(i.cb);
    let text = match catch_unwind(AssertUnwindSafe(|| i.plugin.parameter_string(&host, id))) {
        Ok(t) => t,
        Err(_) => return E_FAIL,
    };
    match text {
        None => E_NOTIMPL,
        Some(s) => {
            let bytes = s.as_bytes();
            let cap = (out_param_size as usize) - 1;
            let n = bytes.len().min(cap);
            ptr::copy_nonoverlapping(bytes.as_ptr(), out_param as *mut u8, n);
            *out_param.add(n) = 0;
            S_OK
        }
    }
}

#[allow(clippy::extra_unused_type_parameters)] // kept for vtable-construction uniformity
unsafe extern "C" fn on_get_user_interface_shim<V, X, P: VdjPlugin>(
    _this: *mut c_void,
    _iface: *mut TVdjPluginInterface8,
) -> HRESULT {
    // MVP: no custom UI; the host builds the default one from declared
    // parameters (of which the MVP declares none).
    E_NOTIMPL
}

unsafe extern "C" fn on_start_shim<P: DspPlugin>(this: *mut c_void) -> HRESULT {
    let i = inst::<DspSlots, DspFields, P>(this);
    let host = Host::from_cb(i.cb);
    match catch_unwind(AssertUnwindSafe(|| i.plugin.on_start(&host))) {
        Ok(Ok(())) => S_OK,
        Ok(Err(e)) => e.0,
        Err(_) => E_FAIL,
    }
}

unsafe extern "C" fn on_stop_shim<P: DspPlugin>(this: *mut c_void) -> HRESULT {
    let i = inst::<DspSlots, DspFields, P>(this);
    let host = Host::from_cb(i.cb);
    match catch_unwind(AssertUnwindSafe(|| i.plugin.on_stop(&host))) {
        Ok(Ok(())) => S_OK,
        Ok(Err(e)) => e.0,
        Err(_) => E_FAIL,
    }
}

unsafe extern "C" fn on_process_samples_shim<P: DspPlugin>(
    this: *mut c_void,
    buffer: *mut f32,
    nb: i32,
) -> HRESULT {
    let i = inst::<DspSlots, DspFields, P>(this);
    if buffer.is_null() || nb <= 0 {
        return S_OK;
    }
    // Per the header: samples are interleaved stereo, buffer[0..2*nb].
    let samples = std::slice::from_raw_parts_mut(buffer, nb as usize * 2);
    let host = Host::from_cb(i.cb);
    let ctx = DspContext {
        host: &host,
        sample_rate: i.host_fields.sample_rate,
        song_bpm: i.host_fields.song_bpm,
        song_pos_beats: i.host_fields.song_pos_beats,
    };
    let plugin = &mut i.plugin;
    match catch_unwind(AssertUnwindSafe(|| plugin.process_samples(samples, &ctx))) {
        Ok(()) => S_OK,
        Err(_) => E_FAIL,
    }
}

// ---------------------------------------------------------------------------
// Vtable construction and instantiation
// ---------------------------------------------------------------------------

const fn basic_slots_for<V, X, P: VdjPlugin>() -> BasicSlots {
    BasicSlots {
        on_load: on_load_shim::<V, X, P>,
        on_get_plugin_info: on_get_plugin_info_shim::<V, X, P>,
        release: release_shim::<V, X, P>,
        dtor_complete: dtor_complete_shim::<V, X, P>,
        dtor_deleting: dtor_deleting_shim::<V, X, P>,
        on_parameter: on_parameter_shim::<V, X, P>,
        on_get_parameter_string: on_get_parameter_string_shim::<V, X, P>,
        on_get_user_interface: on_get_user_interface_shim::<V, X, P>,
    }
}

const fn dsp_slots<P: DspPlugin>() -> DspSlots {
    DspSlots {
        base: basic_slots_for::<DspSlots, DspFields, P>(),
        on_start: on_start_shim::<P>,
        on_stop: on_stop_shim::<P>,
        on_process_samples: on_process_samples_shim::<P>,
    }
}

/// Allocate an instance and aim its vptr at the vtable stored inside the same
/// allocation (which sidesteps Rust's lack of generic statics). The address is
/// fixed once `Box::into_raw` has run, so the vptr is written after that.
unsafe fn create_instance<V, X: Default, P: VdjPlugin>(slots: V) -> *mut c_void {
    let boxed: Box<Instance<V, X, P>> = Box::new(Instance {
        vptr: ptr::null(),
        hinstance: ptr::null_mut(),
        cb: ptr::null_mut(),
        host_fields: X::default(),
        vtbl: VtblStorage {
            offset_to_top: 0,
            typeinfo: ptr::null(),
            slots,
        },
        info: None,
        plugin: P::new(),
    });
    let raw = Box::into_raw(boxed);
    (*raw).vptr = ptr::addr_of!((*raw).vtbl.slots) as *const c_void;
    raw as *mut c_void
}

/// `DllGetClassObject` body for a basic (headless / AutoStart) plugin.
///
/// The host probes the same export repeatedly, once per interface, in a fixed
/// order, and stops at the first acceptance — so declining with
/// `CLASS_E_CLASSNOTAVAILABLE` (-1) is the normal path, not an error.
///
/// # Safety
/// Called by VirtualDJ with valid GUID references; pointers are null-checked.
pub unsafe fn dll_get_class_object_basic<P: VdjPlugin>(
    rclsid: *const Guid,
    riid: *const Guid,
    pp_object: *mut *mut c_void,
) -> HRESULT {
    dispatch(rclsid, riid, pp_object, &IID_IVDJPLUGINBASIC8, || {
        create_instance::<BasicSlots, NoFields, P>(basic_slots_for::<BasicSlots, NoFields, P>())
    })
}

/// `DllGetClassObject` body for a Sound Effect (DSP) plugin.
///
/// # Safety
/// Called by VirtualDJ with valid GUID references; pointers are null-checked.
pub unsafe fn dll_get_class_object_dsp<P: DspPlugin>(
    rclsid: *const Guid,
    riid: *const Guid,
    pp_object: *mut *mut c_void,
) -> HRESULT {
    dispatch(rclsid, riid, pp_object, &IID_IVDJPLUGINDSP8, || {
        create_instance::<DspSlots, DspFields, P>(dsp_slots::<P>())
    })
}

unsafe fn dispatch(
    rclsid: *const Guid,
    riid: *const Guid,
    pp_object: *mut *mut c_void,
    accepted: &Guid,
    make: impl FnOnce() -> *mut c_void,
) -> HRESULT {
    if rclsid.is_null() || riid.is_null() || pp_object.is_null() {
        return CLASS_E_CLASSNOTAVAILABLE;
    }
    if *rclsid != CLSID_VDJPLUGIN8 || *riid != *accepted {
        return CLASS_E_CLASSNOTAVAILABLE;
    }
    match catch_unwind(AssertUnwindSafe(make)) {
        Ok(obj) => {
            *pp_object = obj;
            NO_ERROR
        }
        Err(_) => E_FAIL,
    }
}

// ---------------------------------------------------------------------------
// Offset sanity, independent of the SDK headers
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;
    use std::mem::{offset_of, size_of};

    struct Dummy;
    impl VdjPlugin for Dummy {
        fn new() -> Self {
            Dummy
        }
        fn info(&self) -> PluginInfo {
            PluginInfo::default()
        }
    }

    #[test]
    fn host_visible_prefix_offsets() {
        // The C++ object: vptr @0, hInstance @8, cb @16, subclass fields @24.
        assert_eq!(offset_of!(BasicInstance<Dummy>, vptr), 0);
        assert_eq!(offset_of!(BasicInstance<Dummy>, hinstance), 8);
        assert_eq!(offset_of!(BasicInstance<Dummy>, cb), 16);
        assert_eq!(offset_of!(DspInstance<Dummy>, host_fields), 24);
        // DSP fields: SampleRate @+0, SongBpm @+4, SongPosBeats @+8; the C++
        // IVdjPluginDsp8 is 40 bytes, so our host-visible prefix must end there.
        assert_eq!(offset_of!(DspFields, sample_rate), 0);
        assert_eq!(offset_of!(DspFields, song_bpm), 4);
        assert_eq!(offset_of!(DspFields, song_pos_beats), 8);
        assert_eq!(offset_of!(DspInstance<Dummy>, host_fields) + size_of::<DspFields>(), 40);
    }

    #[test]
    #[allow(clippy::erasing_op, clippy::identity_op)] // `0 * 8` spells out the slot index
    fn vtable_slot_offsets() {
        // Declaration order with the two destructor slots at 3 and 4.
        assert_eq!(offset_of!(BasicSlots, on_load), 0 * 8);
        assert_eq!(offset_of!(BasicSlots, on_get_plugin_info), 1 * 8);
        assert_eq!(offset_of!(BasicSlots, release), 2 * 8);
        assert_eq!(offset_of!(BasicSlots, dtor_complete), 3 * 8);
        assert_eq!(offset_of!(BasicSlots, dtor_deleting), 4 * 8);
        assert_eq!(offset_of!(BasicSlots, on_parameter), 5 * 8);
        assert_eq!(offset_of!(BasicSlots, on_get_parameter_string), 6 * 8);
        assert_eq!(offset_of!(BasicSlots, on_get_user_interface), 7 * 8);
        assert_eq!(offset_of!(DspSlots, on_start), 8 * 8);
        assert_eq!(offset_of!(DspSlots, on_stop), 9 * 8);
        assert_eq!(offset_of!(DspSlots, on_process_samples), 10 * 8);
    }

    #[test]
    fn guid_is_lp64_shaped() {
        // unsigned long Data1 on LP64 → 24 bytes, not the 16-byte Windows GUID.
        assert_eq!(size_of::<Guid>(), 24);
    }
}

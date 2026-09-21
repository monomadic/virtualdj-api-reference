//! Raw ABI definitions mirroring the Atomix Plugin SDK 8 headers (`vdjPlugin8.h`,
//! `vdjDsp8.h`) on macOS.
//!
//! Everything here is byte-layout-critical. The shapes are verified against the
//! real headers by the C++ reference harness in `tests/layout.rs`, and the
//! documented loading path itself is verified live in
//! `docs/Plugin SDK.md` §"Loading" (VirtualDJ 2026, macOS arm64).

use std::ffi::{c_char, c_void};

/// `SInt32` on macOS (the header's own typedef).
pub type HRESULT = i32;

pub const S_OK: HRESULT = 0;
pub const S_FALSE: HRESULT = 1;
pub const NO_ERROR: HRESULT = 0;
pub const E_NOTIMPL: HRESULT = 0x8000_4001_u32 as i32;
pub const E_FAIL: HRESULT = 0x8000_4005_u32 as i32;
pub const E_INVALIDARG: HRESULT = 0x8007_0057_u32 as i32;
/// The header's macOS branch defines this as plain `-1`, not the COM value.
pub const CLASS_E_CLASSNOTAVAILABLE: HRESULT = -1;

/// The SDK's GUID struct as compiled on macOS.
///
/// The header declares `Data1` as `unsigned long`, which is **8 bytes** on LP64
/// macOS — so this is a 24-byte struct, not the 16-byte Windows GUID. VirtualDJ
/// itself is compiled against the same header, so both sides agree. Verified by
/// the layout harness (`sizeof_guid`).
#[repr(C)]
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub struct Guid {
    pub data1: u64,
    pub data2: u16,
    pub data3: u16,
    pub data4: [u8; 8],
}

pub const CLSID_VDJPLUGIN8: Guid = Guid {
    data1: 0xED8A_8D87,
    data2: 0xF4F9,
    data3: 0x4DCD,
    data4: [0xBD, 0x24, 0x29, 0x14, 0x12, 0xE9, 0x3B, 0x60],
};
pub const IID_IVDJPLUGINBASIC8: Guid = Guid {
    data1: 0xa1d9_0ea1,
    data2: 0x4d0d,
    data3: 0x42dd,
    data4: [0xa4, 0xd0, 0xb8, 0xf3, 0x37, 0xb3, 0x21, 0xf1],
};
pub const IID_IVDJPLUGINSTARTSTOP8: Guid = Guid {
    data1: 0xa1d9_1ea1,
    data2: 0x4e0d,
    data3: 0x32dd,
    data4: [0x14, 0xd0, 0xc8, 0xf3, 0x47, 0xb6, 0x41, 0xd1],
};
pub const IID_IVDJPLUGINDSP8: Guid = Guid {
    data1: 0x7cfc_f3f5,
    data2: 0x6fb9,
    data3: 0x434c,
    data4: [0xb6, 0x03, 0xd7, 0x3a, 0x88, 0xf6, 0x72, 0x26],
};
pub const IID_IVDJPLUGINBUFFER8: Guid = Guid {
    data1: 0x1d00_e65f,
    data2: 0x44c7,
    data3: 0x41bf,
    data4: [0xa3, 0x6b, 0x04, 0xda, 0xf2, 0x67, 0x3b, 0x98],
};

// Parameter type constants (`VDJPARAM_*`).
pub const VDJPARAM_BUTTON: i32 = 0;
pub const VDJPARAM_SLIDER: i32 = 1;
pub const VDJPARAM_SWITCH: i32 = 2;
pub const VDJPARAM_STRING: i32 = 3;
pub const VDJPARAM_CUSTOM: i32 = 4;
pub const VDJPARAM_RADIO: i32 = 5;
pub const VDJPARAM_COMMAND: i32 = 6;
pub const VDJPARAM_COLORFX: i32 = 7;
pub const VDJPARAM_BEATS: i32 = 8;
pub const VDJPARAM_BEATS_RELATIVE: i32 = 9;
pub const VDJPARAM_POSITION: i32 = 10;
pub const VDJPARAM_RELEASEFX: i32 = 11;
pub const VDJPARAM_TRANSITIONFX: i32 = 12;

// Plugin info flags (`VDJFLAG_*`).
pub const VDJFLAG_NODOCK: u32 = 0x1;
pub const VDJFLAG_PROCESSAFTERSTOP: u32 = 0x2;
pub const VDJFLAG_PROCESSFIRST: u32 = 0x4;
pub const VDJFLAG_PROCESSLAST: u32 = 0x8;
/// Set *by VirtualDJ* before `OnGetPluginInfo` when the passed struct is the
/// extended (`TVdjPluginInfo8_Extension1`) type.
pub const VDJFLAG_EXTENSION1: u32 = 0x10;
pub const VDJFLAG_SETPREVIEW: u32 = 0x20;
pub const VDJFLAG_POSITION_NOSLIP: u32 = 0x40;
pub const VDJFLAG_ALWAYSPREFADER: u32 = 0x80;
pub const VDJFLAG_ALWAYSPOSTFADER: u32 = 0x100;
pub const VDJFLAG_EPHEMERAL: u32 = 0x200;

// Interface type selectors for `TVdjPluginInterface8.type_`.
pub const VDJINTERFACE_DEFAULT: u32 = 0;
pub const VDJINTERFACE_SKIN: u32 = 1;
pub const VDJINTERFACE_DIALOG: u32 = 2;

/// `TVdjPluginInfo8`. On macOS `VDJ_BITMAP` is `char *`.
#[repr(C)]
pub struct TVdjPluginInfo8 {
    pub plugin_name: *const c_char,
    pub author: *const c_char,
    pub description: *const c_char,
    pub version: *const c_char,
    pub bitmap: *mut c_char,
    pub flags: u32,
}

/// `TVdjPluginInterface8`. On macOS `VDJ_WINDOW` is `void *` (an `NSWindow *`).
#[repr(C)]
pub struct TVdjPluginInterface8 {
    pub type_: u32,
    pub xml: *const c_char,
    pub image_buffer: *mut c_void,
    pub image_size: i32,
    pub h_wnd: *mut c_void,
}

/// Vtable of the host-supplied `IVdjCallbacks8` (pure-virtual, no destructor,
/// no data members — the clean direction of the ABI).
///
/// macOS `VDJ_API` is empty, so these are plain C-convention calls with `this`
/// as the first argument. Slot order is declaration order; verified by the
/// layout harness via pointer-to-member decoding.
#[repr(C)]
pub struct IVdjCallbacks8Vtbl {
    pub send_command:
        unsafe extern "C" fn(this: *mut IVdjCallbacks8, command: *const c_char) -> HRESULT,
    pub get_info: unsafe extern "C" fn(
        this: *mut IVdjCallbacks8,
        command: *const c_char,
        result: *mut f64,
    ) -> HRESULT,
    pub get_string_info: unsafe extern "C" fn(
        this: *mut IVdjCallbacks8,
        command: *const c_char,
        result: *mut c_void,
        size: i32,
    ) -> HRESULT,
    pub declare_parameter: unsafe extern "C" fn(
        this: *mut IVdjCallbacks8,
        parameter: *mut c_void,
        type_: i32,
        id: i32,
        name: *const c_char,
        short_name: *const c_char,
        default_value: f32,
    ) -> HRESULT,
    pub get_song_buffer: unsafe extern "C" fn(
        this: *mut IVdjCallbacks8,
        pos: i32,
        nb: i32,
        buffer: *mut *mut i16,
    ) -> HRESULT,
}

/// An `IVdjCallbacks8 *` as handed to the plugin: a pointer to a vtable pointer.
#[repr(C)]
pub struct IVdjCallbacks8 {
    pub vtbl: *const IVdjCallbacks8Vtbl,
}

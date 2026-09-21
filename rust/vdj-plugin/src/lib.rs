//! Write VirtualDJ plugins in Rust.
//!
//! A safe wrapper over the Atomix Plugin SDK 8 C++ ABI, for macOS. MVP scope:
//! **basic (headless / AutoStart) plugins** and **Sound Effect (DSP) plugins**.
//!
//! ```ignore
//! use vdj_plugin::{DspContext, DspPlugin, Host, PluginInfo, VdjPlugin};
//!
//! struct Gain;
//!
//! impl VdjPlugin for Gain {
//!     fn new() -> Self { Gain }
//!     fn info(&self) -> PluginInfo {
//!         PluginInfo { name: "Rust Gain".into(), ..PluginInfo::default() }
//!     }
//! }
//!
//! impl DspPlugin for Gain {
//!     fn process_samples(&mut self, buffer: &mut [f32], _ctx: &DspContext) {
//!         for s in buffer { *s *= 0.5 }
//!     }
//! }
//!
//! vdj_plugin::export_dsp_plugin!(Gain);
//! ```
//!
//! The generated `DllGetClassObject` follows VirtualDJ's live-verified loading
//! contract (see the reference repo's `docs/Plugin SDK.md`): the host probes
//! one export with a sequence of interface IDs and the plugin declares its
//! type by which IID it accepts.
//!
//! # Verification
//!
//! The ABI layer (vtable slot order, the double destructor slot, host-poked
//! field offsets, the LP64 GUID) is asserted two ways: pure-Rust offset tests,
//! and `tests/layout.rs`, which compiles a C++ reference program against the
//! real SDK headers and diffs every offset and vtable slot index. Run it with
//! the headers available under `vendor/` (or `VDJ_SDK=<dir>`).

#[cfg(not(target_os = "macos"))]
compile_error!(
    "vdj-plugin currently targets macOS only: the vtable and GUID layouts baked in here \
     are the Itanium-ABI / LP64 shapes verified against VirtualDJ on macOS."
);

pub mod host;
pub mod sys;
pub mod wrapper;

mod export;

pub use host::{Host, Result, SharedHost, VdjError};

/// What `OnGetPluginInfo` reports to VirtualDJ. The strings are copied into
/// storage owned by the plugin instance, so they may be built dynamically.
#[derive(Clone, Debug, Default)]
pub struct PluginInfo {
    pub name: String,
    pub author: String,
    pub description: String,
    pub version: String,
    /// `sys::VDJFLAG_*` bits.
    pub flags: u32,
}

/// Base plugin behavior (`IVdjPlugin8`).
///
/// Lifecycle, as observed live: the object is created during type negotiation,
/// the host writes its callback pointer, then calls `OnGetPluginInfo` (once)
/// and `OnLoad` (once). A *basic* plugin in `AutoStart/` is then a headless
/// service — VirtualDJ never calls into it again — so long-running work starts
/// from [`on_load`](VdjPlugin::on_load), typically on its own thread with a
/// [`SharedHost`]. A recognized functional type (DSP) additionally gets its
/// `OnStart`/`OnStop`/`OnProcessSamples`/`OnParameter` driven.
///
/// `on_load` fires early in app startup: queries about state that is not ready
/// yet (the browser, decks) return `E_INVALIDARG` *at that moment* — retry
/// later rather than concluding the query is invalid.
pub trait VdjPlugin: Sized + 'static {
    /// Construct the plugin. Called during `DllGetClassObject`, before the
    /// host has attached its callbacks — no [`Host`] is available here.
    fn new() -> Self;

    /// Identity for `OnGetPluginInfo`.
    fn info(&self) -> PluginInfo;

    fn on_load(&mut self, host: &Host) -> Result<()> {
        let _ = host;
        Ok(())
    }

    /// A declared parameter changed from within VirtualDJ. (The MVP does not
    /// yet declare parameters, so this only fires once that lands.)
    fn on_parameter(&mut self, host: &Host, id: i32) -> Result<()> {
        let _ = (host, id);
        Ok(())
    }

    /// The string label VirtualDJ shows for a parameter; `None` → `E_NOTIMPL`,
    /// letting the host use its default rendering.
    fn parameter_string(&mut self, host: &Host, id: i32) -> Option<String> {
        let _ = (host, id);
        None
    }
}

/// Per-buffer context for [`DspPlugin::process_samples`], snapshotting the
/// host-written `IVdjPluginDsp8` fields.
pub struct DspContext<'a> {
    pub host: &'a Host,
    /// Audio engine sample rate (44100 observed live).
    pub sample_rate: i32,
    /// **Samples between two consecutive beats**, not beats per minute. Reads
    /// as a 120 BPM default (22050) while the deck is idle.
    pub song_bpm: i32,
    /// Beats since the song's first beat, at the start of this buffer.
    pub song_pos_beats: f64,
}

/// A Sound Effect (`IVdjPluginDsp8`).
pub trait DspPlugin: VdjPlugin {
    fn on_start(&mut self, host: &Host) -> Result<()> {
        let _ = host;
        Ok(())
    }

    fn on_stop(&mut self, host: &Host) -> Result<()> {
        let _ = host;
        Ok(())
    }

    /// Process one interleaved-stereo buffer in place: `buffer.len() == 2 * nb`
    /// frames, `[L, R, L, R, …]`. Real-time audio path: do not allocate, block,
    /// or call the host here if avoidable. A panic is caught at the ABI
    /// boundary and reported to the host as `E_FAIL`.
    fn process_samples(&mut self, buffer: &mut [f32], ctx: &DspContext);
}

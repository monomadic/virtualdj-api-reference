//! Safe wrappers around the host's `IVdjCallbacks8` interface.

use crate::sys::*;
use std::ffi::{c_void, CString};
use std::fmt;

/// A failed host call, carrying the raw `HRESULT`.
///
/// Any non-negative `HRESULT` (`S_OK`, `S_FALSE`) is success; anything negative
/// is an error. VirtualDJ writes `0.0` into `GetInfo`'s out-parameter even on
/// failure, so the `HRESULT` — not the value — is always the authoritative
/// answer (see `docs/Plugin SDK.md`).
#[derive(Clone, Copy, PartialEq, Eq)]
pub struct VdjError(pub HRESULT);

impl VdjError {
    pub fn code(&self) -> HRESULT {
        self.0
    }
}

impl fmt::Debug for VdjError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "VdjError({:#010x})", self.0 as u32)
    }
}

impl fmt::Display for VdjError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let name = match self.0 {
            E_NOTIMPL => " (E_NOTIMPL)",
            E_FAIL => " (E_FAIL)",
            E_INVALIDARG => " (E_INVALIDARG)",
            _ => "",
        };
        write!(f, "host call failed: HRESULT {:#010x}{name}", self.0 as u32)
    }
}

impl std::error::Error for VdjError {}

pub type Result<T> = std::result::Result<T, VdjError>;

fn check(hr: HRESULT) -> Result<HRESULT> {
    if hr >= 0 {
        Ok(hr)
    } else {
        Err(VdjError(hr))
    }
}

fn to_cstring(s: &str) -> Result<CString> {
    CString::new(s).map_err(|_| VdjError(E_INVALIDARG))
}

/// Default buffer size for [`Host::get_string_info`]. `GetStringInfo` takes an
/// explicit size, and nothing in the SDK documents a maximum result length.
const STRING_INFO_BUF: usize = 8192;

/// Handle to the VirtualDJ host, valid for the duration of a callback.
///
/// Borrowed (`&Host`) into every trait method, so a plugin cannot accidentally
/// store it past the call. For a background thread (a bridge server, a
/// companion process launcher), take [`Host::shared`] — with its caveats.
pub struct Host {
    cb: *mut IVdjCallbacks8,
}

impl Host {
    /// # Safety
    /// `cb` must be the host-written callback pointer from a live plugin
    /// instance (or null, which makes every call return `E_FAIL`).
    pub(crate) unsafe fn from_cb(cb: *mut IVdjCallbacks8) -> Host {
        Host { cb }
    }

    fn vtbl(&self) -> Result<(*mut IVdjCallbacks8, &IVdjCallbacks8Vtbl)> {
        if self.cb.is_null() {
            return Err(VdjError(E_FAIL));
        }
        unsafe {
            let vt = (*self.cb).vtbl;
            if vt.is_null() {
                return Err(VdjError(E_FAIL));
            }
            Ok((self.cb, &*vt))
        }
    }

    /// Execute a VDJScript action (`SendCommand`). This is the execute channel:
    /// it changes live VirtualDJ state.
    pub fn send_command(&self, command: &str) -> Result<()> {
        let (cb, vt) = self.vtbl()?;
        let c = to_cstring(command)?;
        check(unsafe { (vt.send_command)(cb, c.as_ptr()) }).map(|_| ())
    }

    /// Numeric query (`GetInfo`). Every numeric VDJScript result — booleans,
    /// counts, 0..1 sliders — comes back through this single `double` channel.
    pub fn get_info(&self, query: &str) -> Result<f64> {
        self.get_info_raw(query).and_then(|(hr, v)| check(hr).map(|_| v))
    }

    /// `GetInfo` preserving the raw `(HRESULT, value)` pair. The value is
    /// written even on failure (as `0.0`), so introspection-style callers need
    /// both halves.
    pub fn get_info_raw(&self, query: &str) -> Result<(HRESULT, f64)> {
        let (cb, vt) = self.vtbl()?;
        let c = to_cstring(query)?;
        let mut value: f64 = 0.0;
        let hr = unsafe { (vt.get_info)(cb, c.as_ptr(), &mut value) };
        Ok((hr, value))
    }

    /// Text query (`GetStringInfo`), decoded as UTF-8 (lossily — the host is
    /// UTF-8 but this crate does not trust it to be).
    pub fn get_string_info(&self, query: &str) -> Result<String> {
        let (hr, s) = self.get_string_info_raw(query, STRING_INFO_BUF)?;
        check(hr).map(|_| s)
    }

    /// `GetStringInfo` with an explicit buffer size, preserving the raw
    /// `HRESULT` alongside whatever the host wrote.
    pub fn get_string_info_raw(&self, query: &str, buf_size: usize) -> Result<(HRESULT, String)> {
        let (cb, vt) = self.vtbl()?;
        let c = to_cstring(query)?;
        let mut buf = vec![0u8; buf_size.max(2)];
        let hr = unsafe {
            (vt.get_string_info)(cb, c.as_ptr(), buf.as_mut_ptr() as *mut c_void, buf.len() as i32)
        };
        let end = buf.iter().position(|&b| b == 0).unwrap_or(buf.len());
        buf.truncate(end);
        Ok((hr, String::from_utf8_lossy(&buf).into_owned()))
    }

    /// A `Send + Sync` copy of this handle for use off the callback thread.
    pub fn shared(&self) -> SharedHost {
        SharedHost { cb: self.cb }
    }
}

/// A host handle usable from any thread, for background services (the pattern
/// VirtualDJ's own Network Control plugin embodies).
///
/// **Evidence status:** the SDK documents nothing about callback thread-safety.
/// One recorded session (`docs/VDJScript Local Test Tracker.md`, 2026-08-15)
/// ran 55 `GetInfo`/`GetStringInfo` probes from a detached non-main thread with
/// no misbehavior. That is evidence, not a guarantee; keep off-thread use to
/// query calls where possible and route `send_command` through short strings.
#[derive(Clone, Copy)]
pub struct SharedHost {
    cb: *mut IVdjCallbacks8,
}

// SAFETY: forwarding raw calls into the host, which one recorded session showed
// tolerating cross-thread callers (see type docs). The pointer itself is set
// once by the host before OnLoad and never changes for the instance's life.
unsafe impl Send for SharedHost {}
unsafe impl Sync for SharedHost {}

impl SharedHost {
    fn as_host(&self) -> Host {
        Host { cb: self.cb }
    }

    pub fn send_command(&self, command: &str) -> Result<()> {
        self.as_host().send_command(command)
    }

    pub fn get_info(&self, query: &str) -> Result<f64> {
        self.as_host().get_info(query)
    }

    pub fn get_info_raw(&self, query: &str) -> Result<(HRESULT, f64)> {
        self.as_host().get_info_raw(query)
    }

    pub fn get_string_info(&self, query: &str) -> Result<String> {
        self.as_host().get_string_info(query)
    }

    pub fn get_string_info_raw(&self, query: &str, buf_size: usize) -> Result<(HRESULT, String)> {
        self.as_host().get_string_info_raw(query, buf_size)
    }
}

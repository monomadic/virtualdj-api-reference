//! Entry-point macros. Exactly one `export_*_plugin!` invocation per cdylib.

/// Export a basic (headless / AutoStart) plugin: accepts
/// `IID_IVdjPluginBasic8` and declines everything else.
#[macro_export]
macro_rules! export_basic_plugin {
    ($ty:ty) => {
        #[no_mangle]
        pub unsafe extern "C" fn DllGetClassObject(
            rclsid: *const $crate::sys::Guid,
            riid: *const $crate::sys::Guid,
            pp_object: *mut *mut ::std::ffi::c_void,
        ) -> $crate::sys::HRESULT {
            $crate::wrapper::dll_get_class_object_basic::<$ty>(rclsid, riid, pp_object)
        }
    };
}

/// Export a Sound Effect (DSP) plugin: accepts `IID_IVdjPluginDsp8`.
#[macro_export]
macro_rules! export_dsp_plugin {
    ($ty:ty) => {
        #[no_mangle]
        pub unsafe extern "C" fn DllGetClassObject(
            rclsid: *const $crate::sys::Guid,
            riid: *const $crate::sys::Guid,
            pp_object: *mut *mut ::std::ffi::c_void,
        ) -> $crate::sys::HRESULT {
            $crate::wrapper::dll_get_class_object_dsp::<$ty>(rclsid, riid, pp_object)
        }
    };
}

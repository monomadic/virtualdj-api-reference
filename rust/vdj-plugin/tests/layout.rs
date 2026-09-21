//! The layout harness: compile `layout_ref.cpp` against the real Atomix SDK
//! headers and diff every offset, size, and vtable slot index against this
//! crate's `#[repr(C)]` definitions.
//!
//! Needs the SDK headers (not vendored — no license grant; see the repo's
//! `docs/Plugin SDK.md`). Looked up via `VDJ_SDK=<dir>` or by searching
//! `../../vendor/` for `vdjDsp8.h`. Without them the test skips, loudly.

use std::collections::HashMap;
use std::mem::{offset_of, size_of};
use std::path::PathBuf;
use std::process::Command;

use vdj_plugin::sys::{Guid, IVdjCallbacks8Vtbl, TVdjPluginInfo8, TVdjPluginInterface8};
use vdj_plugin::wrapper::{BasicSlots, DspSlots};

fn find_sdk() -> Option<PathBuf> {
    if let Ok(dir) = std::env::var("VDJ_SDK") {
        let p = PathBuf::from(dir);
        if p.join("vdjDsp8.h").exists() {
            return Some(p);
        }
    }
    // vendor/ lives at the repo root, two levels above this crate.
    let vendor = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../vendor");
    let mut stack = vec![vendor];
    while let Some(dir) = stack.pop() {
        let Ok(entries) = std::fs::read_dir(&dir) else { continue };
        for e in entries.flatten() {
            let p = e.path();
            if p.is_dir() {
                stack.push(p);
            } else if p.file_name().is_some_and(|n| n == "vdjDsp8.h") {
                return p.parent().map(PathBuf::from);
            }
        }
    }
    None
}

fn reference_values() -> Option<HashMap<String, i64>> {
    let sdk = match find_sdk() {
        Some(s) => s,
        None => {
            eprintln!(
                "SKIP: Atomix SDK headers not found (set VDJ_SDK or put them under vendor/); \
                 the C++ cross-check did not run"
            );
            return None;
        }
    };
    let src = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/layout_ref.cpp");
    let out = PathBuf::from(env!("CARGO_TARGET_TMPDIR")).join("layout_ref");
    let compile = Command::new("clang++")
        .args(["-std=c++17", "-O0", "-Wno-invalid-offsetof", "-I"])
        .arg(&sdk)
        .arg(&src)
        .arg("-o")
        .arg(&out)
        .output()
        .expect("failed to run clang++ (Command Line Tools required for the cross-check)");
    assert!(
        compile.status.success(),
        "layout_ref.cpp failed to compile:\n{}",
        String::from_utf8_lossy(&compile.stderr)
    );
    let run = Command::new(&out).output().expect("failed to run layout_ref");
    assert!(run.status.success(), "layout_ref exited nonzero");
    let mut map = HashMap::new();
    for line in String::from_utf8_lossy(&run.stdout).lines() {
        let mut it = line.split_whitespace();
        if let (Some(k), Some(v)) = (it.next(), it.next()) {
            map.insert(k.to_string(), v.parse::<i64>().expect("numeric value"));
        }
    }
    Some(map)
}

#[test]
fn layout_matches_the_real_headers() {
    let Some(r) = reference_values() else { return };
    let get = |k: &str| -> i64 { *r.get(k).unwrap_or_else(|| panic!("missing key {k}")) };

    // Any -1 means a pointer-to-member decoded as non-virtual: harness broken.
    for (k, v) in &r {
        assert!(*v >= 0, "{k} decoded as {v}");
    }

    assert_eq!(get("ptr_size"), 8);
    assert_eq!(get("sizeof_guid"), size_of::<Guid>() as i64, "LP64 GUID");

    // TVdjPluginInfo8 / TVdjPluginInterface8 shapes.
    assert_eq!(get("sizeof_plugininfo"), size_of::<TVdjPluginInfo8>() as i64);
    assert_eq!(get("info_name_off"), offset_of!(TVdjPluginInfo8, plugin_name) as i64);
    assert_eq!(get("info_author_off"), offset_of!(TVdjPluginInfo8, author) as i64);
    assert_eq!(get("info_description_off"), offset_of!(TVdjPluginInfo8, description) as i64);
    assert_eq!(get("info_version_off"), offset_of!(TVdjPluginInfo8, version) as i64);
    assert_eq!(get("info_bitmap_off"), offset_of!(TVdjPluginInfo8, bitmap) as i64);
    assert_eq!(get("info_flags_off"), offset_of!(TVdjPluginInfo8, flags) as i64);
    assert_eq!(get("sizeof_plugininterface"), size_of::<TVdjPluginInterface8>() as i64);
    assert_eq!(get("iface_type_off"), offset_of!(TVdjPluginInterface8, type_) as i64);
    assert_eq!(get("iface_xml_off"), offset_of!(TVdjPluginInterface8, xml) as i64);
    assert_eq!(get("iface_image_off"), offset_of!(TVdjPluginInterface8, image_buffer) as i64);
    assert_eq!(get("iface_imagesize_off"), offset_of!(TVdjPluginInterface8, image_size) as i64);
    assert_eq!(get("iface_hwnd_off"), offset_of!(TVdjPluginInterface8, h_wnd) as i64);

    // The host-poked data members of the plugin object. The Rust Instance's
    // own offsets are asserted in wrapper.rs unit tests against these same
    // constants, closing the loop.
    assert_eq!(get("sizeof_ivdjplugin8"), 24);
    assert_eq!(get("plugin_hinstance_off"), 8);
    assert_eq!(get("plugin_cb_off"), 16);
    assert_eq!(get("sizeof_dsp"), 40);
    assert_eq!(get("dsp_samplerate_off"), 24);
    assert_eq!(get("dsp_songbpm_off"), 28);
    assert_eq!(get("dsp_songposbeats_off"), 32);

    // Plugin vtable slot order, including the implicit 2-slot destructor gap
    // (Release at 2, OnParameter at 5).
    let basic = |off: usize| (off / 8) as i64;
    assert_eq!(get("slot_onload"), basic(offset_of!(BasicSlots, on_load)));
    assert_eq!(get("slot_ongetplugininfo"), basic(offset_of!(BasicSlots, on_get_plugin_info)));
    assert_eq!(get("slot_release"), basic(offset_of!(BasicSlots, release)));
    assert_eq!(get("slot_onparameter"), basic(offset_of!(BasicSlots, on_parameter)));
    assert_eq!(
        get("slot_ongetparameterstring"),
        basic(offset_of!(BasicSlots, on_get_parameter_string))
    );
    assert_eq!(
        get("slot_ongetuserinterface"),
        basic(offset_of!(BasicSlots, on_get_user_interface))
    );
    assert_eq!(get("dsp_slot_onstart"), basic(offset_of!(DspSlots, on_start)));
    assert_eq!(get("dsp_slot_onstop"), basic(offset_of!(DspSlots, on_stop)));
    assert_eq!(get("dsp_slot_onprocesssamples"), basic(offset_of!(DspSlots, on_process_samples)));

    // StartStop shares the DSP's OnStart/OnStop positions (both append to the
    // same 8-slot base) — recorded for the day a StartStop wrapper lands.
    assert_eq!(get("ss_slot_onstart"), basic(offset_of!(DspSlots, on_start)));
    assert_eq!(get("ss_slot_onstop"), basic(offset_of!(DspSlots, on_stop)));

    // Host callback interface slots.
    assert_eq!(get("cb_slot_sendcommand"), basic(offset_of!(IVdjCallbacks8Vtbl, send_command)));
    assert_eq!(get("cb_slot_getinfo"), basic(offset_of!(IVdjCallbacks8Vtbl, get_info)));
    assert_eq!(
        get("cb_slot_getstringinfo"),
        basic(offset_of!(IVdjCallbacks8Vtbl, get_string_info))
    );
    assert_eq!(
        get("cb_slot_declareparameter"),
        basic(offset_of!(IVdjCallbacks8Vtbl, declare_parameter))
    );
    assert_eq!(get("cb_slot_getsongbuffer"), basic(offset_of!(IVdjCallbacks8Vtbl, get_song_buffer)));
}

//! Rust Tremolo — the vdj-plugin MVP validation vehicle.
//!
//! A Sound Effect that dips the volume once per beat, driven by the
//! host-written `SongPosBeats`/`SongBpm` fields, so a listener can verify both
//! the audio path and the host-poked field offsets by ear. `OnLoad` writes a
//! small log proving the callback ABI round-trips (`get_version` through both
//! typed query channels).
//!
//! Install: `rust/package.sh tremolo --install`, then restart VirtualDJ and
//! select "Rust Tremolo" in a deck's effects list.

use std::f64::consts::TAU;
use std::io::Write;

use vdj_plugin::{DspContext, DspPlugin, Host, PluginInfo, Result, VdjPlugin};

struct Tremolo;

fn log_path() -> Option<std::path::PathBuf> {
    let home = std::env::var_os("HOME")?;
    Some(
        std::path::PathBuf::from(home)
            .join("Library/Application Support/VirtualDJ/rust-tremolo.log"),
    )
}

fn log_line(text: &str) {
    let Some(path) = log_path() else { return };
    if let Ok(mut f) = std::fs::OpenOptions::new().create(true).append(true).open(path) {
        let _ = writeln!(f, "{text}");
    }
}

impl VdjPlugin for Tremolo {
    fn new() -> Self {
        Tremolo
    }

    fn info(&self) -> PluginInfo {
        PluginInfo {
            name: "Rust Tremolo".into(),
            author: "vdj-plugin".into(),
            description: "Beat-synced tremolo written in Rust (vdj-plugin MVP)".into(),
            version: env!("CARGO_PKG_VERSION").into(),
            flags: 0,
        }
    }

    fn on_load(&mut self, host: &Host) -> Result<()> {
        // Prove both typed query channels round-trip through the Rust ABI
        // layer. get_version is a text-channel query; GetInfo on it records
        // whatever HRESULT the numeric channel answers — both halves are the
        // interesting part, so raw variants are used.
        let text = host.get_string_info_raw("get_version", 256);
        let num = host.get_info_raw("get_version");
        log_line(&format!("loaded: GetStringInfo(get_version)={text:?} GetInfo(get_version)={num:?}"));
        Ok(())
    }
}

impl DspPlugin for Tremolo {
    fn on_start(&mut self, _host: &Host) -> Result<()> {
        log_line("started");
        Ok(())
    }

    fn on_stop(&mut self, _host: &Host) -> Result<()> {
        log_line("stopped");
        Ok(())
    }

    fn process_samples(&mut self, buffer: &mut [f32], ctx: &DspContext) {
        // song_bpm is samples-between-beats (22050 default when idle → the
        // tremolo free-runs at 120 BPM on an idle deck, by design of the host).
        let samples_per_beat = ctx.song_bpm.max(1) as f64;
        let mut beat = ctx.song_pos_beats;
        let step = 1.0 / samples_per_beat;
        for frame in buffer.chunks_exact_mut(2) {
            // Full gain on the beat, dipping to 0.35 halfway through it.
            let gain = (0.675 + 0.325 * (TAU * beat.fract()).cos()) as f32;
            frame[0] *= gain;
            frame[1] *= gain;
            beat += step;
        }
    }
}

vdj_plugin::export_dsp_plugin!(Tremolo);

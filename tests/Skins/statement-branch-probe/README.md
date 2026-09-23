# Debug button calibration attempt

Build 18.0.9644, arm64, desktop skin, 2026-09-24. This synthetic fixture was
loaded and the first button (`debug 42`) clicked at CUA coordinates `[650,118]`.
[The immediate screenshot](direct-debug-no-popup.png) showed the main fixture,
not a popup. **This is not a negative debug result.** The debug log appeared
later; timing/window visibility was not calibrated. No subsequent buttons were
tested and no statement was classified from silence.

The [journal](run-9644.jsonl) records loading, restored original skin and empty
stopped decks, and byte-checked removal of the installation. The fixture remains
available for reproduction via the shared runner. Only round one was installed.
See [Statement Branch Probe](../../../docs/Statement%20Branch%20Probe.md) for the
completed HTTP marker/debug calibration and its differing evidence.

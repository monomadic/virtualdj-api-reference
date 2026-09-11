"""Stopped long-track time readers; phase controls, independent repeats and restoration."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import time

from fixtures import Channel, FixtureError, build_fixtures, establish, is_error

ARTIFACT = Path(__file__).resolve().parents[1] / "tests/long-time-forms.json"
SECONDS = 7500
VERBS = ("get_time", "get_time_hour", "get_time_min", "get_time_sec",
         "get_time_ms", "get_time_msf", "get_time_sign")
FORMS = ("", "elapsed", "remain", "total", "absolute", "zzqqx", "vfnrbq")


def audio():
    path = Path(tempfile.gettempdir()) / "vdj-long-time-7500.flac"
    if not path.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                        f"anullsrc=r=8000:cl=mono:d={SECONDS}", "-c:a", "flac", str(path)], check=True)
    duration = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=nw=1:nk=1", str(path)], text=True))
    if abs(duration - SECONDS) > .01:
        raise FixtureError("generated duration differs from fixture specification")
    return path


def q(ch, script):
    return ch.query("deck 1 " + script)


def mode(ch):
    modes = [m for m in ("elapsed", "remain", "total") if q(ch, f"display_time '{m}'") == "yes"]
    if len(modes) != 1:
        raise FixtureError("display mode has no unique readback")
    return modes[0]


def wait(ch, script, predicate):
    until = time.monotonic() + 30
    while True:
        value = q(ch, script)
        if predicate(value):
            return value
        if time.monotonic() > until:
            raise FixtureError(f"readback failed: {script} = {value}")
        time.sleep(.1)


def set_mode(ch, desired):
    # Repeating a one-mode display_time write toggles away from that mode.
    if mode(ch) != desired:
        ch.execute(f"deck 1 display_time '{desired}'")
    wait(ch, f"display_time '{desired}'", lambda v: v == "yes")


def classify(runs):
    result = {}
    for verb in VERBS:
        result[verb] = {}
        for form in FORMS[1:5]:
            separating = []
            for run in runs:
                phases = []
                for phase in run["phases"]:
                    values = phase["readings"][verb]
                    stable = all(len(set(v)) == 1 for v in values.values())
                    a, b = values["zzqqx"][0], values["vfnrbq"][0]
                    v = values[form][0]
                    if stable and a == b and v != a and not is_error(v):
                        phases.append(phase["id"])
                separating.append(phases)
            result[verb][form] = {"verdict": "recognized" if all(separating) else "undiscriminated",
                                  "separates_in": separating}
    # Account for the documented default without claiming discrimination.
    hour_phases = [p for run in runs for p in run["phases"]]
    if hour_phases and all(
            all(int(v) == int(float(p["position"]) / 1000 /
                (1 + float(p["pitch_percent"]) / 100) / 3600)
                for form in ("elapsed", "zzqqx", "vfnrbq")
                for v in p["readings"]["get_time_hour"][form]) for p in hour_phases):
        result["get_time_hour"]["elapsed"]["verdict"] = "names-elapsed-fallback"
    return result


def run(ch, path, number):
    fixture = build_fixtures(path)["long_time"]
    before = {"pitch": q(ch, "pitch"), "mode": mode(ch)}
    print(f"run {number}: saved pitch={before['pitch']}, display_time={before['mode']}", flush=True)
    # Fail before any writes if the fixture cannot be restored by unloading.
    for assertion in fixture.preconditions:
        if not assertion.check(ch)[0]:
            raise FixtureError(assertion.describes)
    phases = []
    try:
        establish(ch, fixture, verbose=False)
        wait(ch, 'get_loaded_song "fullpath"', lambda v: v == str(path))
        settings = [(4200, 100, "elapsed"), (4200, 100, "remain"),
                    (3750, 112, "elapsed"), (3750, 112, "remain"),
                    (4207.125, 100, "remain")]
        for seconds, pitch, display in settings if number == 1 else reversed(settings):
            ch.execute(f"deck 1 pitch {pitch}%")
            ch.execute(f"deck 1 goto {seconds / SECONDS * 100:.9f}%")
            set_mode(ch, display)
            position = wait(ch, "get_position & param_multiply 7500000",
                            lambda v: abs(float(v) - seconds * 1000) < 10)
            pitch_value = wait(ch, "get_pitch", lambda v: abs(float(v) - (pitch - 100)) < .05)
            if mode(ch) != display or q(ch, "play") != "no":
                raise FixtureError("phase is not stopped in the requested display mode")
            readings = {}
            for verb in VERBS:
                readings[verb] = {f: [] for f in FORMS}
                for order in (FORMS, tuple(reversed(FORMS))):
                    for form in order:
                        readings[verb][form].append(q(ch, verb + (f" '{form}'" if form else "")))
            phases.append({"id": f"{seconds}s-{pitch}pct-{display}", "position": position,
                           "pitch_percent": pitch_value, "display_time": display,
                           "readings": readings})
    finally:
        ch.execute("deck 1 unload")
        wait(ch, "loaded", lambda v: v == "no")
        ch.execute(f"deck 1 pitch {before['pitch']}")
        set_mode(ch, before["mode"])
        wait(ch, "pitch", lambda v: abs(float(v) - float(before['pitch'])) < .00001)
        restored = (q(ch, "loaded") == "no" and q(ch, "play") == "no"
                    and abs(float(q(ch, "pitch")) - float(before["pitch"])) < .00001
                    and mode(ch) == before["mode"])
        if not restored:
            raise FixtureError("restoration failed; aborting")
    return {"run": number, "phases": phases, "restored": restored}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--reclassify", action="store_true")
    ap.add_argument("--get", metavar="VERB", help="read a result; empty name reports all verdicts")
    args = ap.parse_args()
    if args.get is not None:
        data = json.loads(ARTIFACT.read_text())
        print(json.dumps({"summary": data["summary"], "forms": data["verbs"].get(args.get)
                          if args.get else data["verbs"]}, indent=1))
        return
    if args.check or args.reclassify:
        data = json.loads(ARTIFACT.read_text())
        if args.reclassify:
            data["verbs"] = classify(data["runs"])
            ARTIFACT.write_text(json.dumps(data, indent=1) + "\n")
        assert len(data["runs"]) == 2 and all(r["restored"] for r in data["runs"])
        assert data["summary"]["build"].isdigit()
        assert data["verbs"] == classify(data["runs"])
        for run_data in data["runs"]:
            for phase in run_data["phases"]:
                elapsed = float(phase["position"]) / 1000
                remain = SECONDS - elapsed
                speed = 1 + float(phase["pitch_percent"]) / 100
                displayed = elapsed if phase["display_time"] == "elapsed" else remain
                expected = {"": int(displayed / speed / 3600),
                            "elapsed": int(elapsed / speed / 3600),
                            "remain": int(remain / speed / 3600),
                            "total": int(SECONDS / speed / 3600),
                            "absolute": int(displayed / 3600)}
                for form, hours in expected.items():
                    assert all(int(v) == hours for v in phase["readings"]["get_time_hour"][form])
        print("long-time capture: recomputed verdicts and restoration check passed")
        return
    if not args.run:
        ap.error("choose --run or --check")
    ch = Channel()
    provenance = ch.provenance()
    path = audio()
    runs = [run(ch, path, n) for n in (1, 2)]
    payload = {"summary": provenance, "method": {"duration_seconds": SECONDS,
               "duration_oracle": "ffprobe of generated FLAC", "position_oracle": "get_position & param_multiply 7500000 (milliseconds)",
               "pitch_oracle": "get_pitch", "controls": ["zzqqx", "vfnrbq"]},
               "runs": runs, "verbs": classify(runs)}
    tmp = ARTIFACT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=1) + "\n")
    tmp.replace(ARTIFACT)
    print(json.dumps(payload["verbs"], indent=1))


if __name__ == "__main__":
    main()

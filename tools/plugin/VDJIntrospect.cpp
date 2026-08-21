//////////////////////////////////////////////////////////////////////////
//
// VDJIntrospect — a READ-ONLY VirtualDJ introspection plugin.
//
// Purpose (TODO.md task 10a): call the host's two typed query callbacks on a
// list of probe strings and record the NATIVE results — the raw HRESULT, the
// `double` (with its exact bit pattern), and the UTF-8 buffer — instead of the
// single flattened string the HTTP control interface returns.
//
// SAFETY CONTRACT — this plugin never changes VirtualDJ state:
//   * It never calls SendCommand(). The call is not present in this file, so
//     no probe list, however malformed, can reach execute position.
//   * GetInfo() and GetStringInfo() are query-position only.
//   * It reads its probe lists and writes its results and log under its own
//     working directory. It touches nothing else on disk.
//
// Execute-position testing, if it ever happens, belongs in a separate plugin
// built behind an explicit switch — not here.
//
// The Atomix SDK headers this compiles against are NOT vendored in this repo
// (no license grant); see docs/Plugin SDK.md and the .gitignore entry.
//
//////////////////////////////////////////////////////////////////////////

// Two builds from one source. The default is the headless AutoStart probe. With
// -DVDJINTROSPECT_DSP it becomes a Sound Effect instead — which matters because
// VirtualDJ's Extensions list is organised by *functional type* (Skins, Effects,
// Samples, Pads, Other), and a plugin that answers only to IVdjPluginBasic8 is
// none of them, so it is loaded but never listed and never given a surface.
// Being a real effect is the cheapest way to acquire one; a video FX plugin is
// the alternative and needs video output.
//
// -DVDJINTROSPECT_SKIN layers onto the DSP build: the effect then answers
// OnGetUserInterface with VDJINTERFACE_SKIN, handing VirtualDJ a skin XML buffer
// and a PNG. The buffers are re-read FROM DISK on every call rather than baked
// into the bundle, because that is the whole point — if VirtualDJ asks more than
// once, editing skin.xml and re-opening the panel replaces the restart-per-edit
// cycle that makes skin questions expensive. Still read-only: no SendCommand.
#ifdef VDJINTROSPECT_DSP
#include "vdjDsp8.h"
#else
#include "vdjPlugin8.h"
#endif

#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <cmath>
#include <string>
#include <vector>
#include <ctime>
#include <atomic>
#include <chrono>
#include <memory>
#include <thread>
#include <sys/stat.h>
#include <sys/time.h>
#include <pwd.h>
#include <unistd.h>

// HRESULTs are recorded raw, as signed 32-bit ints, and named on the python side
// (tools/plugin_introspect.py) — the mac branch of vdjPlugin8.h defines only
// S_OK / S_FALSE / E_NOTIMPL, and an unrecognised code must survive the capture
// rather than be flattened into "unknown" here.

#define VDJINTROSPECT_VERSION "0.1.0"

//////////////////////////////////////////////////////////////////////////
// Working directory: ~/Library/Application Support/VirtualDJ/VDJIntrospect/
//
//   probes.txt      input  — one probe string per line; '#' comments, blanks skipped
//   results.json    output — one record per probe
//   probes-late.txt input  — optional; if present, swept again 40s AFTER load, so
//                            late-initializing subsystems (the browser) get a fair
//                            chance to answer
//   results-late.json output — the delayed run
//   go.txt          input  — touch it (`just plugin-go`) and the delayed list is
//                            swept again within ~2s, no restart needed; this is
//                            how prepared-state captures are taken
//   plugin.log   output — append-only lifecycle log (also written when there is
//                         no probes.txt, so a failed load is still diagnosable)

static std::string HomeDir()
{
    const char *home = getenv("HOME");
    if (home && *home) return std::string(home);
    struct passwd *pw = getpwuid(getuid());
    return pw && pw->pw_dir ? std::string(pw->pw_dir) : std::string("/tmp");
}

static std::string WorkDir()
{
    return HomeDir() + "/Library/Application Support/VirtualDJ/VDJIntrospect";
}

static std::string WorkPath(const char *leaf)
{
    return WorkDir() + "/" + leaf;
}

static void Log(const char *fmt, ...)
{
    mkdir(WorkDir().c_str(), 0755);
    FILE *f = fopen(WorkPath("plugin.log").c_str(), "a");
    if (!f) return;

    time_t now = time(NULL);
    struct tm tm_utc;
    gmtime_r(&now, &tm_utc);
    char stamp[32];
    strftime(stamp, sizeof(stamp), "%Y-%m-%dT%H:%M:%SZ", &tm_utc);
    fprintf(f, "%s ", stamp);

    va_list args;
    va_start(args, fmt);
    vfprintf(f, fmt, args);
    va_end(args);

    fputc('\n', f);
    fclose(f);
}

// Every IID the public SDK publishes. Only vdjPlugin8.h is included (so the build
// needs one header), but VirtualDJ type-probes a plugin with the IIDs from all
// four, and an unnamed GUID in the log is worthless — so the rest are transcribed
// here, each from the header named beside it.
static const struct { const char *name; GUID iid; } kKnownIIDs[] = {
    {"IVdjPluginBasic8",     IID_IVdjPluginBasic8},     // vdjPlugin8.h
    {"IVdjPluginStartStop8", IID_IVdjPluginStartStop8}, // vdjPlugin8.h
    {"IVdjPluginDsp8",       {0x7cfcf3f5,0x6fb9,0x434c,{0xb6,0x03,0xd7,0x3a,0x88,0xf6,0x72,0x26}}}, // vdjDsp8.h
    {"IVdjPluginBuffer8",    {0x1d00e65f,0x44c7,0x41bf,{0xa3,0x6b,0x04,0xda,0xf2,0x67,0x3b,0x98}}}, // vdjDsp8.h
    {"IVdjPluginVideoFx8",   {0xbf1876aa,0x3cbd,0x404a,{0xbe,0xab,0x5f,0x8b,0x51,0xe3,0x90,0xc0}}}, // vdjVideo8.h
    {"IVdjPluginVideoTransition8",          {0x2f350983,0xf88f,0x429c,{0x87,0x75,0x62,0x87,0x68,0x7d,0xe0,0xd7}}}, // vdjVideo8.h
    {"IVdjPluginVideoTransitionMultiDeck8", {0x54d0e81c,0x51a6,0x49b0,{0x82,0x3f,0x75,0x91,0x76,0xf1,0xcf,0x06}}}, // vdjVideo8.h
    {"IVdjPluginOnlineSource",              {0x85d20f05,0x0ccf,0x4cab,{0xaa,0x50,0x1c,0x04,0xea,0xb6,0xb8,0x5d}}}, // vdjOnlineSource.h
};

static const char *IIDName(const GUID &g)
{
    for (size_t i = 0; i < sizeof(kKnownIIDs) / sizeof(kKnownIIDs[0]); i++)
        if (memcmp(&g, &kKnownIIDs[i].iid, sizeof(GUID)) == 0) return kKnownIIDs[i].name;
    return "UNDOCUMENTED";
}

static std::string FormatGuid(const GUID &g)
{
    char buf[64];
    snprintf(buf, sizeof(buf), "%08lX-%04X-%04X-%02X%02X%02X%02X%02X%02X%02X%02X",
             (unsigned long)g.Data1, g.Data2, g.Data3,
             g.Data4[0], g.Data4[1], g.Data4[2], g.Data4[3],
             g.Data4[4], g.Data4[5], g.Data4[6], g.Data4[7]);
    return std::string(buf);
}

//////////////////////////////////////////////////////////////////////////
// JSON emission (hand-rolled: no dependencies inside the host process)

static void JsonEscape(FILE *f, const char *s, size_t len)
{
    for (size_t i = 0; i < len; i++)
    {
        unsigned char c = (unsigned char)s[i];
        switch (c)
        {
            case '"':  fputs("\\\"", f); break;
            case '\\': fputs("\\\\", f); break;
            case '\b': fputs("\\b", f); break;
            case '\f': fputs("\\f", f); break;
            case '\n': fputs("\\n", f); break;
            case '\r': fputs("\\r", f); break;
            case '\t': fputs("\\t", f); break;
            default:
                // Non-UTF8-safe bytes are escaped rather than emitted raw, so a
                // binary answer (handshake returns 128 raw bytes) cannot corrupt
                // the artifact.
                if (c < 0x20 || c >= 0x7f) fprintf(f, "\\u%04x", c);
                else fputc(c, f);
        }
    }
}

static void JsonString(FILE *f, const std::string &s)
{
    fputc('"', f);
    JsonEscape(f, s.data(), s.size());
    fputc('"', f);
}

//////////////////////////////////////////////////////////////////////////
// OnKey / mouse callbacks — the only channel that might carry PRESS vs RELEASE.
//
// `while_pressed` and the whole down/up half of the mapper contract are recorded
// as "not established" in docs/Mapper XML.md for one reason: HTTP has no press.
// It can only ask "is it playing?", never "was this button just pushed?". This
// interface is the first thing in reach that is event-driven, and `OnKey`'s
// undocumented `flag` parameter is the candidate for the press/release bit.
//
// Reached via the EXTENDED info struct: VirtualDJ sets VDJFLAG_EXTENSION1 on the
// way into OnGetPluginInfo (confirmed on this build, 2026-08-15), which means the
// pointer is really a TVdjPluginInfo8_Extension1 carrying a mouseCallbacks slot.
//
// SAFETY: every handler returns false — "not handled". Returning true would
// SWALLOW the input, and a plugin that eats the user's keystrokes and clicks is
// exactly the kind of side effect this plugin promises not to have. The mouse
// handlers exist only because the interface requires them; they record nothing
// but a count, so ordinary mouse movement cannot flood the log.

static void LogEvent(const char *json_body)
{
    mkdir(WorkDir().c_str(), 0755);
    FILE *f = fopen(WorkPath("keylog.jsonl").c_str(), "a");
    if (!f) return;
    struct timeval tv;
    gettimeofday(&tv, NULL);
    fprintf(f, "{\"t\": %ld.%06d, %s}\n", (long)tv.tv_sec, (int)tv.tv_usec, json_body);
    fclose(f);
}

struct CVDJMouseKeys : public IVdjVideoMouseCallbacks8
{
    std::atomic<int> moves{0};

    bool OnMouseMove(int x, int y, int buttons, int keyModifiers)
    {
        // Counted, not logged: a move handler that wrote a line per event would
        // produce megabytes and tell us nothing new.
        moves++;
        return false;
    }

    bool OnMouseDown(int x, int y, int buttons, int keyModifiers)
    {
        char buf[256];
        snprintf(buf, sizeof(buf),
                 "\"event\": \"mousedown\", \"x\": %d, \"y\": %d, "
                 "\"buttons\": %d, \"modifiers\": %d, \"moves_so_far\": %d",
                 x, y, buttons, keyModifiers, moves.load());
        LogEvent(buf);
        return false;
    }

    bool OnMouseUp(int x, int y, int buttons, int keyModifiers)
    {
        char buf[256];
        snprintf(buf, sizeof(buf),
                 "\"event\": \"mouseup\", \"x\": %d, \"y\": %d, "
                 "\"buttons\": %d, \"modifiers\": %d",
                 x, y, buttons, keyModifiers);
        LogEvent(buf);
        return false;
    }

    void OnKey(const char *ch, int vkey, int modifiers, int flag, int scancode)
    {
        // `ch` is undocumented as to encoding and lifetime, so it is escaped as
        // bytes rather than trusted as a C string beyond a bounded length.
        std::string text;
        if (ch) for (int i = 0; i < 16 && ch[i]; i++) text.push_back(ch[i]);

        FILE *f = fopen(WorkPath("keylog.jsonl").c_str(), "a");
        if (!f) return;
        struct timeval tv;
        gettimeofday(&tv, NULL);
        fprintf(f, "{\"t\": %ld.%06d, \"event\": \"key\", \"ch\": ",
                (long)tv.tv_sec, (int)tv.tv_usec);
        JsonString(f, text);
        fprintf(f, ", \"ch_null\": %s", ch ? "false" : "true");
        fprintf(f, ", \"vkey\": %d, \"modifiers\": %d, \"flag\": %d, \"scancode\": %d}\n",
                vkey, modifiers, flag, scancode);
        fclose(f);
    }
};

static CVDJMouseKeys g_mousekeys;

//////////////////////////////////////////////////////////////////////////
// GetSongBuffer — the PCM of the loaded song, at any position.
//
// This callback has no equivalent on any other channel: HTTP, Remote, the binary
// and the XML corpora all stop at metadata. It is the input side of every
// waveform question in docs/Skin Waveforms.md.
//
// Nothing about its units is documented — whether `pos` and `nb` count samples,
// frames, or milliseconds, whether the buffer is mono or interleaved stereo, and
// who owns the memory. So the probe does not assume: it asks for the same span at
// deliberately overlapping positions and records enough per request (leading
// samples, min/max, RMS, a hash, and an even/odd channel comparison) to settle
// the units offline, from the data rather than from a guess.
//
// Read-only: GetSongBuffer is a getter, and nothing here writes through the
// returned pointer.

struct TBufferRequest { int pos; int nb; };

static std::vector<std::string> ReadProbeFile(const char *leaf, bool *found);

static void SweepSongBuffer(IVdjCallbacks8 *cb, const char *outLeaf)
{
    bool found = false;
    std::vector<std::string> lines = ReadProbeFile("songbuffer.txt", &found);
    if (!found) return;

    std::vector<TBufferRequest> reqs;
    for (size_t i = 0; i < lines.size(); i++)
    {
        int pos = 0, nb = 0;
        if (sscanf(lines[i].c_str(), "%d %d", &pos, &nb) != 2) continue;
        // Cap the span: the host may return fewer samples than asked without
        // saying so, and a huge nb would turn that into an overread.
        if (nb < 1) nb = 1;
        if (nb > 4096) nb = 4096;
        reqs.push_back({pos, nb});
    }
    if (reqs.empty()) return;

    FILE *out = fopen(WorkPath(outLeaf).c_str(), "w");
    if (!out) { Log("ERROR: cannot write %s", outLeaf); return; }

    time_t now = time(NULL);
    struct tm tm_utc;
    gmtime_r(&now, &tm_utc);
    char stamp[32];
    strftime(stamp, sizeof(stamp), "%Y-%m-%dT%H:%M:%SZ", &tm_utc);

    char title[512]; title[0] = 0;
    cb->GetStringInfo("get_title", title, (int)sizeof(title));
    char filepath[1024]; filepath[0] = 0;
    cb->GetStringInfo("get_filepath", filepath, (int)sizeof(filepath));
    double totaltime = -1, songpos = -1, bpm = -1;
    cb->GetInfo("get_totaltime", &totaltime);
    cb->GetInfo("get_position", &songpos);
    cb->GetInfo("get_bpm", &bpm);

    fprintf(out, "{\n  \"tool\": \"VDJIntrospect\",\n  \"probe\": \"GetSongBuffer\",\n");
    fprintf(out, "  \"tool_version\": \"%s\",\n", VDJINTROSPECT_VERSION);
    fprintf(out, "  \"captured_utc\": \"%s\",\n", stamp);
    fprintf(out, "  \"song_title\": "); JsonString(out, std::string(title));
    fprintf(out, ",\n  \"song_filepath\": "); JsonString(out, std::string(filepath));
    fprintf(out, ",\n  \"get_totaltime\": %.17g", totaltime);
    fprintf(out, ",\n  \"get_position\": %.17g", songpos);
    fprintf(out, ",\n  \"get_bpm\": %.17g", bpm);
    fprintf(out, ",\n  \"requests\": [\n");

    for (size_t i = 0; i < reqs.size(); i++)
    {
        short *buffer = NULL;
        HRESULT hr = cb->GetSongBuffer(reqs[i].pos, reqs[i].nb, &buffer);

        fprintf(out, "    {\"pos\": %d, \"nb\": %d, \"hresult\": %ld, \"buffer_null\": %s",
                reqs[i].pos, reqs[i].nb, (long)(int32_t)hr, buffer ? "false" : "true");

        // The POINTER settles what the head samples only imply. If successive
        // positions return addresses into one persistent decoded buffer, the
        // byte delta per unit of `pos` is the unit — no inference needed. (The
        // absolute value is ASLR noise; only differences within a run mean
        // anything, which is why every request records it.)
        if (buffer) fprintf(out, ", \"ptr\": \"0x%016llx\"", (unsigned long long)(uintptr_t)buffer);

        if (hr == S_OK && buffer)
        {
            long long sum = 0, sumsq = 0, sumsq_even = 0, sumsq_odd = 0;
            int mn = 32767, mx = -32768;
            uint64_t hash = 1469598103934665603ULL;   // FNV-1a
            for (int k = 0; k < reqs[i].nb; k++)
            {
                short v = buffer[k];
                sum += v;
                sumsq += (long long)v * v;
                if (k & 1) sumsq_odd += (long long)v * v; else sumsq_even += (long long)v * v;
                if (v < mn) mn = v;
                if (v > mx) mx = v;
                hash = (hash ^ (uint16_t)v) * 1099511628211ULL;
            }
            fprintf(out, ", \"min\": %d, \"max\": %d", mn, mx);
            fprintf(out, ", \"mean\": %.6f", (double)sum / reqs[i].nb);
            fprintf(out, ", \"rms\": %.6f", sqrt((double)sumsq / reqs[i].nb));
            // If the buffer is interleaved stereo these two differ far less than
            // if it is mono; either way the numbers are recorded, not judged here.
            // `null` rather than a NaN when the span is too short to have both
            // parities — NaN is not valid JSON and would poison the artifact.
            int n_even = (reqs[i].nb + 1) / 2, n_odd = reqs[i].nb / 2;
            if (n_even > 0) fprintf(out, ", \"rms_even\": %.6f", sqrt((double)sumsq_even / n_even));
            else            fprintf(out, ", \"rms_even\": null");
            if (n_odd > 0)  fprintf(out, ", \"rms_odd\": %.6f", sqrt((double)sumsq_odd / n_odd));
            else            fprintf(out, ", \"rms_odd\": null");
            fprintf(out, ", \"hash\": \"0x%016llx\"", (unsigned long long)hash);
            fprintf(out, ", \"head\": [");
            for (int k = 0; k < 16 && k < reqs[i].nb; k++)
                fprintf(out, "%s%d", k ? ", " : "", buffer[k]);
            fprintf(out, "]");
            // The tail lets a later request's head be matched against an earlier
            // request's end, which is how the span length gets checked.
            fprintf(out, ", \"tail\": [");
            for (int k = (reqs[i].nb > 16 ? reqs[i].nb - 16 : 0); k < reqs[i].nb; k++)
                fprintf(out, "%s%d", (k == (reqs[i].nb > 16 ? reqs[i].nb - 16 : 0)) ? "" : ", ",
                        buffer[k]);
            fprintf(out, "]");
        }
        fprintf(out, "}%s\n", (i + 1 < reqs.size()) ? "," : "");
    }

    fprintf(out, "  ]\n}\n");
    fclose(out);
    Log("song-buffer probe done: %zu requests -> %s", reqs.size(), outLeaf);
}

//////////////////////////////////////////////////////////////////////////

// Shared with the delayed-sweep thread. The thread outlives nothing on purpose:
// it checks `alive` (cleared in the destructor) before touching `cb`, so an
// unload during the wait ends the sweep instead of using a dead pointer.
struct TLateState
{
    std::atomic<bool> alive{true};
    IVdjCallbacks8 *cb = NULL;
};

class CVDJIntrospect : public IVdjPluginStartStop8
{
public:
    ~CVDJIntrospect();
    HRESULT VDJ_API OnLoad();
    HRESULT VDJ_API OnGetPluginInfo(TVdjPluginInfo8 *info);
    HRESULT VDJ_API OnStart();
    HRESULT VDJ_API OnStop();
    HRESULT VDJ_API OnGetUserInterface(TVdjPluginInterface8 *pluginInterface);
    HRESULT VDJ_API OnParameter(int id);
    HRESULT VDJ_API OnGetParameterString(int id, char *outParam, int outParamSize);

    // Declared parameters. Every one of the 173 shipped native_*.ini manifests
    // declares parameters, and parameters are what give a plugin a settings
    // panel — so this is the test of whether "headless" is inherent to this
    // plugin type or just a consequence of declaring nothing. Values are read by
    // VirtualDJ, never written by us.
    enum { ID_PROBE_SWITCH = 0, ID_PROBE_SLIDER = 1 };
    int m_probe_switch = 0;
    float m_probe_slider = 0.5f;

private:
    bool m_swept = false;
    std::shared_ptr<TLateState> m_late;
    void RunSweep(const char *trigger);
    void StartLateSweep();
};

HRESULT VDJ_API CVDJIntrospect::OnGetPluginInfo(TVdjPluginInfo8 *info)
{
    // Does VirtualDJ pass the EXTENDED info struct to a plain plugin? If it sets
    // VDJFLAG_EXTENSION1 (0x10) on the way in, the struct is really a
    // TVdjPluginInfo8_Extension1 and carries a mouseCallbacks slot — the only
    // documented route to OnKey, and therefore to press/release, which the mapper
    // contract still lacks. Answered YES on this build, so the callbacks below
    // are installed rather than merely logged.
    Log("OnGetPluginInfo incoming Flags=0x%x extension1=%s",
        (unsigned)info->Flags, (info->Flags & 0x10) ? "YES" : "no");

    // Claim the mouse/key callbacks when the extended struct is offered. This is
    // the whole point of the build: see the OnKey block above.
    bool extended = (info->Flags & 0x10) != 0;
    if (extended)
    {
        TVdjPluginInfo8_Extension1 *ext = (TVdjPluginInfo8_Extension1 *)info;
        ext->mouseCallbacks = &g_mousekeys;
        Log("mouseCallbacks installed — OnKey events will land in keylog.jsonl");
    }

    info->PluginName  = "VDJIntrospect";
    info->Author      = "virtualdj-api-reference";
    info->Description = "Read-only VDJScript query introspection. Never sends commands.";
    info->Version     = VDJINTROSPECT_VERSION;
    info->Bitmap      = NULL;
    // EPHEMERAL (0x200): declare no parameters, keep no .ini. The EXTENSION1 bit
    // is preserved rather than cleared — VirtualDJ set it to describe the struct
    // it passed, so overwriting it would be answering a question it did not ask.
    info->Flags       = 0x200 | (extended ? 0x10 : 0);
    return S_OK;
}

HRESULT VDJ_API CVDJIntrospect::OnLoad()
{
    Log("OnLoad  version=%s pid=%d", VDJINTROSPECT_VERSION, (int)getpid());

    // Declared during OnLoad, as the SDK requires. If VirtualDJ starts calling
    // OnParameter or OnGetUserInterface after this, the UI path is open and the
    // headless lifecycle was self-inflicted.
    HRESULT hr_sw = DeclareParameterSwitch(&m_probe_switch, ID_PROBE_SWITCH,
                                           "Probe Switch", "Probe", false);
    HRESULT hr_sl = DeclareParameterSlider(&m_probe_slider, ID_PROBE_SLIDER,
                                           "Probe Slider", "Slide", 0.5f);
    Log("DeclareParameterSwitch -> %ld, DeclareParameterSlider -> %ld",
        (long)(int32_t)hr_sw, (long)(int32_t)hr_sl);
    RunSweep("OnLoad");
    return S_OK;
}

// Which lifecycle callbacks does a basic AutoStart plugin actually receive? The
// keylog came back empty even though mouseCallbacks was installed, and the
// difference between "VirtualDJ never asks us anything" and "it asks, but never
// routes input" decides whether a UI-bearing or video plugin would fare better.
HRESULT VDJ_API CVDJIntrospect::OnGetUserInterface(TVdjPluginInterface8 *pluginInterface)
{
    Log("OnGetUserInterface called — VirtualDJ IS asking this plugin for a UI");
    return E_NOTIMPL;   // decline: no UI, same as before
}

HRESULT VDJ_API CVDJIntrospect::OnParameter(int id)
{
    Log("OnParameter id=%d (switch=%d slider=%.3f)",
        id, m_probe_switch, m_probe_slider);
    return S_OK;
}

HRESULT VDJ_API CVDJIntrospect::OnGetParameterString(int id, char *outParam, int outParamSize)
{
    // Called when VirtualDJ wants a label for a parameter — i.e. when something
    // is actually displaying it. That makes this a second, independent signal
    // that a UI exists, separate from OnGetUserInterface.
    Log("OnGetParameterString id=%d — something is DISPLAYING this parameter", id);
    return E_NOTIMPL;
}

HRESULT VDJ_API CVDJIntrospect::OnStart()
{
    Log("OnStart");
    RunSweep("OnStart");
    return S_OK;
}

HRESULT VDJ_API CVDJIntrospect::OnStop()
{
    Log("OnStop");
    return S_OK;
}

// Both OnLoad and OnStart trigger the sweep because which one fires depends on
// the interface VirtualDJ negotiated and the folder the bundle sits in — an open
// question this build is meant to answer. The once-flag keeps it to one run, and
// the log records which trigger won.
static std::vector<std::string> ReadProbeFile(const char *leaf, bool *found)
{
    std::vector<std::string> probes;
    *found = false;

    FILE *f = fopen(WorkPath(leaf).c_str(), "r");
    if (!f) return probes;
    *found = true;

    char line[4096];
    while (fgets(line, sizeof(line), f))
    {
        std::string s(line);
        while (!s.empty() && (s.back() == '\n' || s.back() == '\r')) s.pop_back();
        if (s.empty() || s[0] == '#') continue;
        probes.push_back(s);
    }
    fclose(f);
    return probes;
}

// One sweep, parameterised by file pair so the load-time and delayed runs share
// every line of it. `cb` is passed explicitly rather than read from the plugin
// object, because the delayed run happens on another thread.
static void SweepFiles(IVdjCallbacks8 *cb, const char *inLeaf, const char *outLeaf,
                       const char *trigger)
{
    bool found = false;
    std::vector<std::string> probes = ReadProbeFile(inLeaf, &found);
    if (!found)
    {
        Log("no %s in %s — nothing to do", inLeaf, WorkDir().c_str());
        return;
    }

    FILE *out = fopen(WorkPath(outLeaf).c_str(), "w");
    if (!out) { Log("ERROR: cannot write %s", outLeaf); return; }

    time_t now = time(NULL);
    struct tm tm_utc;
    gmtime_r(&now, &tm_utc);
    char stamp[32];
    strftime(stamp, sizeof(stamp), "%Y-%m-%dT%H:%M:%SZ", &tm_utc);

    fprintf(out, "{\n");
    fprintf(out, "  \"tool\": \"VDJIntrospect\",\n");
    fprintf(out, "  \"tool_version\": \"%s\",\n", VDJINTROSPECT_VERSION);
    fprintf(out, "  \"channel\": \"plugin\",\n");
    fprintf(out, "  \"trigger\": \"%s\",\n", trigger);
    fprintf(out, "  \"captured_utc\": \"%s\",\n", stamp);

    // The host's own version, read through the same channel being characterized.
    char version[512];
    version[0] = 0;
    HRESULT vhr = cb->GetStringInfo("get_version", version, (int)sizeof(version));
    fprintf(out, "  \"host_version\": ");
    JsonString(out, std::string(version));
    fprintf(out, ",\n  \"host_version_hresult\": %ld,\n", (long)(int32_t)vhr);

    fprintf(out, "  \"probes\": [\n");

    for (size_t i = 0; i < probes.size(); i++)
    {
        const std::string &probe = probes[i];

        // Sentinel: a callback that returns an error without touching *result
        // must not be reported as having answered 0.
        double value = -123456789.0;
        const double sentinel = value;
        HRESULT numeric_hr = cb->GetInfo(probe.c_str(), &value);

        char text[8192];
        memset(text, 0, sizeof(text));
        HRESULT text_hr = cb->GetStringInfo(probe.c_str(), text, (int)sizeof(text));

        // Length by scan, not strlen: an answer may legitimately contain NULs
        // (handshake returns a 128-byte RSA block).
        size_t text_len = sizeof(text);
        while (text_len > 0 && text[text_len - 1] == 0) text_len--;

        uint64_t bits;
        memcpy(&bits, &value, sizeof(bits));

        fprintf(out, "    {\"probe\": ");
        JsonString(out, probe);
        fprintf(out, ", \"numeric_hresult\": %ld", (long)(int32_t)numeric_hr);
        fprintf(out, ", \"numeric_written\": %s", (value == sentinel) ? "false" : "true");
        if (value != sentinel)
        {
            fprintf(out, ", \"numeric\": %.17g", value);
            fprintf(out, ", \"numeric_bits\": \"0x%016llx\"", (unsigned long long)bits);
        }
        fprintf(out, ", \"text_hresult\": %ld", (long)(int32_t)text_hr);
        fprintf(out, ", \"text_len\": %zu", text_len);
        fprintf(out, ", \"text\": ");
        fputc('"', out);
        JsonEscape(out, text, text_len);
        fputc('"', out);
        fprintf(out, "}%s\n", (i + 1 < probes.size()) ? "," : "");
    }

    fprintf(out, "  ]\n}\n");
    fclose(out);

    Log("sweep done via %s: %zu probes -> %s", trigger, probes.size(), outLeaf);
}

void CVDJIntrospect::RunSweep(const char *trigger)
{
    if (m_swept) { Log("sweep already done, %s ignored", trigger); return; }
    m_swept = true;
    SweepFiles(cb, "probes.txt", "results.json", trigger);
    StartLateSweep();
}

// The delayed sweep exists because OnLoad fires while VirtualDJ is still starting
// up: anything not yet initialized (the browser, notably) is indistinguishable
// from a verb that never answers. Opt-in by the presence of probes-late.txt, so
// an ordinary capture never spawns a thread.
//
// UNPROVEN: the SDK says nothing about calling the host callbacks off the main
// thread. This is the experiment that finds out. The shared state lets an unload
// during the wait cancel the sweep rather than use a freed `cb`.
void CVDJIntrospect::StartLateSweep()
{
    bool found = false;
    ReadProbeFile("probes-late.txt", &found);
    if (!found) return;

    m_late = std::make_shared<TLateState>();
    m_late->cb = cb;

    std::shared_ptr<TLateState> state = m_late;
    std::thread([state]() {
        // One automatic run, late enough that startup-initialized subsystems
        // (the browser) are up. This is the capture that proved the silent
        // browser readers were a timing artifact.
        for (int i = 0; i < 40 && state->alive; i++)
            std::this_thread::sleep_for(std::chrono::seconds(1));
        if (!state->alive) { Log("late sweep cancelled — plugin unloaded during wait"); return; }
        Log("late sweep starting (40s after load)");
        SweepFiles(state->cb, "probes-late.txt", "results-late.json", "late");

        // Then stay available: re-sweep whenever a trigger file appears. This is
        // what makes prepared-state work possible — set up the app by hand (load
        // a track, highlight a song), then ask for a capture — and it removes the
        // restart that every previous capture cost.
        Log("trigger loop armed — `just plugin-go` re-sweeps without a restart");
        while (state->alive)
        {
            std::this_thread::sleep_for(std::chrono::seconds(2));
            if (!state->alive) break;

            struct stat st;
            if (stat(WorkPath("go.txt").c_str(), &st) != 0) continue;
            unlink(WorkPath("go.txt").c_str());

            Log("trigger seen — sweeping");
            SweepFiles(state->cb, "probes-late.txt", "results-late.json", "trigger");
            SweepSongBuffer(state->cb, "results-songbuffer.json");
        }
        Log("trigger loop ended");
    }).detach();

    Log("late sweep armed");
}

CVDJIntrospect::~CVDJIntrospect()
{
    if (m_late) m_late->alive = false;
}

//////////////////////////////////////////////////////////////////////////
// Entry point.
//
// Answers for BOTH published IIDs and logs every negotiation attempt — which
// (CLSID, IID) pairs VirtualDJ actually asks for is itself an open question
// (docs/Plugin SDK.md, "Loading, and one open question"), and the log is the
// evidence either way.

#ifdef VDJINTROSPECT_DSP
//////////////////////////////////////////////////////////////////////////
// Sound Effect build.
//
// The audio path is a strict PASSTHROUGH: OnProcessSamples does not write to the
// buffer, so enabling this effect cannot alter what the audience hears. It exists
// to be a plugin VirtualDJ recognises as a type — with a panel, and therefore a
// surface that key and mouse events might reach.
//
// It does NOT run the verb sweeps: an effect is instantiated per deck and per
// enable, and re-running a 1,100-probe sweep on each of those would be both
// pointless and slow.

class CVDJIntrospectFX : public IVdjPluginDsp8
{
public:
    HRESULT VDJ_API OnLoad();
    HRESULT VDJ_API OnGetPluginInfo(TVdjPluginInfo8 *info);
    HRESULT VDJ_API OnStart();
    HRESULT VDJ_API OnStop();
    HRESULT VDJ_API OnProcessSamples(float *buffer, int nb);
    HRESULT VDJ_API OnParameter(int id);
#ifdef VDJINTROSPECT_SKIN
    HRESULT VDJ_API OnGetUserInterface(TVdjPluginInterface8 *pluginInterface);
#endif

    int m_probe_switch = 0;
    float m_probe_slider = 0.5f;

private:
    bool m_logged_first_buffer = false;
#ifdef VDJINTROSPECT_SKIN
    // The served buffers must outlive the call: TVdjPluginInterface8 takes a
    // borrowed `const char*` and a raw pointer/size, and the SDK never says when
    // VirtualDJ is done reading them. Holding them as members means they live as
    // long as the plugin instance, which is the only lifetime we can guarantee.
    std::string m_xml;
    std::vector<unsigned char> m_png;
    int m_ui_calls = 0;
#endif
};

HRESULT VDJ_API CVDJIntrospectFX::OnGetPluginInfo(TVdjPluginInfo8 *info)
{
    Log("[FX] OnGetPluginInfo incoming Flags=0x%x extension1=%s",
        (unsigned)info->Flags, (info->Flags & 0x10) ? "YES" : "no");

    bool extended = (info->Flags & 0x10) != 0;
    if (extended)
    {
        ((TVdjPluginInfo8_Extension1 *)info)->mouseCallbacks = &g_mousekeys;
        Log("[FX] mouseCallbacks installed");
    }

#ifdef VDJINTROSPECT_SKIN
    info->PluginName  = "VDJIntrospect Skin";
#else
    info->PluginName  = "VDJIntrospect FX";
#endif
    info->Author      = "virtualdj-api-reference";
    info->Description = "Read-only introspection probe. Audio passthrough — does not alter sound.";
    info->Version     = VDJINTROSPECT_VERSION;
    info->Bitmap      = NULL;
    info->Flags       = extended ? 0x10 : 0;
    return S_OK;
}

HRESULT VDJ_API CVDJIntrospectFX::OnLoad()
{
    Log("[FX] OnLoad");
    DeclareParameterSwitch(&m_probe_switch, 0, "Probe Switch", "Probe", false);
    DeclareParameterSlider(&m_probe_slider, 1, "Probe Slider", "Slide", 0.5f);
    return S_OK;
}

HRESULT VDJ_API CVDJIntrospectFX::OnStart()
{
    // SampleRate is handed to us by the host — an independent check on the
    // 44,100 Hz figure that GetSongBuffer's frame arithmetic implied.
    Log("[FX] OnStart  SampleRate=%d SongBpm=%d SongPosBeats=%.3f",
        SampleRate, SongBpm, SongPosBeats);
    return S_OK;
}

HRESULT VDJ_API CVDJIntrospectFX::OnStop()
{
    Log("[FX] OnStop");
    return S_OK;
}

HRESULT VDJ_API CVDJIntrospectFX::OnParameter(int id)
{
    Log("[FX] OnParameter id=%d (switch=%d slider=%.3f) — VirtualDJ called IN",
        id, m_probe_switch, m_probe_slider);
    return S_OK;
}

HRESULT VDJ_API CVDJIntrospectFX::OnProcessSamples(float *buffer, int nb)
{
    if (!m_logged_first_buffer)
    {
        m_logged_first_buffer = true;
        Log("[FX] first audio buffer: nb=%d SampleRate=%d (PASSTHROUGH, buffer untouched)",
            nb, SampleRate);
    }
    return S_OK;   // touch nothing
}

#ifdef VDJINTROSPECT_SKIN
// Read a whole file into a byte vector. Returns false if it is not there, which
// is a normal state (nothing prepared yet) rather than an error.
static bool ReadWholeFile(const std::string &path, std::vector<unsigned char> &out)
{
    FILE *f = fopen(path.c_str(), "rb");
    if (!f) return false;
    fseek(f, 0, SEEK_END);
    long n = ftell(f);
    fseek(f, 0, SEEK_SET);
    if (n < 0) { fclose(f); return false; }
    out.resize((size_t)n);
    size_t got = n > 0 ? fread(out.data(), 1, (size_t)n, f) : 0;
    fclose(f);
    out.resize(got);
    return true;
}

// The measurement. Three things are being asked at once:
//
//   1. Is OnGetUserInterface called AT ALL on a Sound Effect? Every previous
//      build logged the call and it never fired, but those were plugin types
//      VirtualDJ never gave a surface to.
//   2. If it is called, is it called MORE THAN ONCE — once per panel open, or
//      once per instance? Only the former turns skin testing into a loop.
//   3. Does a skin XML supplied this way actually render?
//
// The XML is re-read from disk each time so that (2), if true, is immediately
// usable. A missing file is served as a built-in placeholder rather than a
// failure, so the first run answers (1) without needing anything prepared.
static const char *kFallbackSkinXml =
    "<Skin name=\"VDJIntrospectSkin\" version=\"8\" width=\"220\" height=\"200\">\n"
    "  <textzone>\n"
    "    <size width=\"200\" height=\"16\"/>\n"
    "    <pos x=\"10\" y=\"10\"/>\n"
    "    <text font=\"arial\" size=\"13\" weight=\"bold\" color=\"white\" align=\"left\"\n"
    "          format=\"NO skin.xml PREPARED\"/>\n"
    "  </textzone>\n"
    "</Skin>\n";

HRESULT VDJ_API CVDJIntrospectFX::OnGetUserInterface(TVdjPluginInterface8 *pluginInterface)
{
    m_ui_calls++;

    std::vector<unsigned char> xml;
    bool have_xml = ReadWholeFile(WorkPath("skin.xml"), xml);
    if (have_xml)
        m_xml.assign((const char *)xml.data(), xml.size());
    else
        m_xml = kFallbackSkinXml;

    bool have_png = ReadWholeFile(WorkPath("skin.png"), m_png);

    pluginInterface->Type        = VDJINTERFACE_SKIN;
    pluginInterface->Xml         = m_xml.c_str();
    pluginInterface->ImageBuffer = have_png && !m_png.empty() ? (void *)m_png.data() : NULL;
    pluginInterface->ImageSize   = have_png ? (int)m_png.size() : 0;

    Log("[SKIN] OnGetUserInterface CALL #%d — serving VDJINTERFACE_SKIN "
        "xml=%s(%zu bytes) png=%s(%zu bytes)",
        m_ui_calls,
        have_xml ? "skin.xml" : "built-in fallback", m_xml.size(),
        have_png ? "skin.png" : "NONE", m_png.size());

    // Record the served XML's first line, so a rendered panel can be matched to
    // the exact revision that produced it without guessing.
    size_t eol = m_xml.find('\n');
    Log("[SKIN]   first line: %s", m_xml.substr(0, eol == std::string::npos ? m_xml.size() : eol).c_str());

    return S_OK;
}
#endif
#endif

extern "C" VDJ_EXPORT HRESULT VDJ_API DllGetClassObject(const GUID &rclsid, const GUID &riid, void **ppObject)
{
    bool clsid_ok = memcmp(&rclsid, &CLSID_VdjPlugin8, sizeof(GUID)) == 0;
    bool basic    = memcmp(&riid, &IID_IVdjPluginBasic8, sizeof(GUID)) == 0;
    bool startstop= memcmp(&riid, &IID_IVdjPluginStartStop8, sizeof(GUID)) == 0;

    Log("DllGetClassObject clsid=%s%s riid=%s (%s)%s",
        FormatGuid(rclsid).c_str(), clsid_ok ? " (CLSID_VdjPlugin8)" : " (UNKNOWN)",
        FormatGuid(riid).c_str(), IIDName(riid),
        (clsid_ok && (basic || startstop)) ? " ACCEPTED" : " declined");

#ifdef VDJINTROSPECT_DSP
    bool dsp = memcmp(&riid, &IID_IVdjPluginDsp8, sizeof(GUID)) == 0;
    if (clsid_ok && dsp)
    {
        *ppObject = (void *)(IVdjPluginDsp8 *)new CVDJIntrospectFX();
        return NO_ERROR;
    }
#else
    if (clsid_ok && (basic || startstop))
    {
        *ppObject = (void *)(IVdjPlugin8 *)new CVDJIntrospect();
        return NO_ERROR;
    }
#endif

    return CLASS_E_CLASSNOTAVAILABLE;
}

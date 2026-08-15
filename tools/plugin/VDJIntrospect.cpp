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

#include "vdjPlugin8.h"

#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <ctime>
#include <atomic>
#include <chrono>
#include <memory>
#include <thread>
#include <sys/stat.h>
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

private:
    bool m_swept = false;
    std::shared_ptr<TLateState> m_late;
    void RunSweep(const char *trigger);
    void StartLateSweep();
};

HRESULT VDJ_API CVDJIntrospect::OnGetPluginInfo(TVdjPluginInfo8 *info)
{
    info->PluginName  = "VDJIntrospect";
    info->Author      = "virtualdj-api-reference";
    info->Description = "Read-only VDJScript query introspection. Never sends commands.";
    info->Version     = VDJINTROSPECT_VERSION;
    info->Bitmap      = NULL;
    // EPHEMERAL: declare no parameters and keep no .ini beside the bundle.
    info->Flags       = 0x200;
    return S_OK;
}

HRESULT VDJ_API CVDJIntrospect::OnLoad()
{
    Log("OnLoad  version=%s pid=%d", VDJINTROSPECT_VERSION, (int)getpid());
    RunSweep("OnLoad");
    return S_OK;
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
        std::this_thread::sleep_for(std::chrono::seconds(40));
        if (!state->alive) { Log("late sweep cancelled — plugin unloaded during wait"); return; }
        Log("late sweep starting (40s after load)");
        SweepFiles(state->cb, "probes-late.txt", "results-late.json", "late");
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

extern "C" VDJ_EXPORT HRESULT VDJ_API DllGetClassObject(const GUID &rclsid, const GUID &riid, void **ppObject)
{
    bool clsid_ok = memcmp(&rclsid, &CLSID_VdjPlugin8, sizeof(GUID)) == 0;
    bool basic    = memcmp(&riid, &IID_IVdjPluginBasic8, sizeof(GUID)) == 0;
    bool startstop= memcmp(&riid, &IID_IVdjPluginStartStop8, sizeof(GUID)) == 0;

    Log("DllGetClassObject clsid=%s%s riid=%s (%s)%s",
        FormatGuid(rclsid).c_str(), clsid_ok ? " (CLSID_VdjPlugin8)" : " (UNKNOWN)",
        FormatGuid(riid).c_str(), IIDName(riid),
        (clsid_ok && (basic || startstop)) ? " ACCEPTED" : " declined");

    if (clsid_ok && (basic || startstop))
    {
        *ppObject = (void *)(IVdjPlugin8 *)new CVDJIntrospect();
        return NO_ERROR;
    }

    return CLASS_E_CLASSNOTAVAILABLE;
}

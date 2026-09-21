//////////////////////////////////////////////////////////////////////////
//
// Offline fake host for Rust-built VirtualDJ plugin bundles.
//
// dlopens the BUILT bundle binary (the exact artifact VirtualDJ loads) and
// drives it through the real SDK headers, so the compiler generates genuine
// Itanium vtable calls against the Rust-laid vtable — negotiation, the
// host-poked data members, info/lifecycle/audio callbacks, and BOTH teardown
// paths (Release() and virtual delete). A watchdog alarm converts any hang
// into a diagnosis naming the stage that wedged, because the live failure
// mode this was written for is a silent hang of VirtualDJ's plugin scan.
//
// Build and run (see rust/README.md):
//   SDK="$(find vendor -name vdjDsp8.h -print -quit)"; SDK="${SDK%/*}"
//   clang++ -std=c++17 -arch arm64 -O0 -g -I "$SDK" \
//       rust/fakehost/fakehost.cpp -o rust/target/fakehost
//   HOME=/tmp/fakehome rust/target/fakehost rust/bundle/RustTremolo.bundle
//
//////////////////////////////////////////////////////////////////////////
#include <cassert>
#include <cmath>
#include <csignal>
#include <cstdio>
#include <cstring>
#include <dlfcn.h>
#include <string>
#include <unistd.h>

#include "vdjDsp8.h"

static const char *stage = "startup";
static int failures = 0;

#define STAGE(s) do { stage = s; printf("== %s ==\n", s); fflush(stdout); } while (0)
#define CHECK(cond, msg) do { \
    if (cond) printf("  ok   %s\n", msg); \
    else { printf("  FAIL %s\n", msg); failures++; } \
} while (0)

static void watchdog(int) {
    // async-signal-safe enough for a diagnostic tool
    char buf[256];
    int n = snprintf(buf, sizeof buf, "\nHANG: watchdog fired during stage '%s'\n", stage);
    write(2, buf, n);
    _exit(2);
}

struct FakeCallbacks : public IVdjCallbacks8 {
    HRESULT SendCommand(const char *c) override {
        printf("  (plugin sent command: %s)\n", c ? c : "(null)");
        return S_OK;
    }
    HRESULT GetInfo(const char *q, double *r) override {
        if (r) *r = 2026.0;
        printf("  (plugin GetInfo: %s)\n", q ? q : "(null)");
        return S_OK;
    }
    HRESULT GetStringInfo(const char *q, void *out, int n) override {
        printf("  (plugin GetStringInfo: %s)\n", q ? q : "(null)");
        if (out && n > 0) snprintf((char *)out, n, "fakehost 1.0");
        return S_OK;
    }
    HRESULT DeclareParameter(void *, int, int, const char *, const char *, float) override {
        return S_OK;
    }
    HRESULT GetSongBuffer(int, int, short **) override { return S_FALSE; }
};

typedef HRESULT (*DllGetClassObjectFn)(const GUID &, const GUID &, void **);

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: fakehost <path-to-.bundle-or-binary>\n");
        return 2;
    }
    signal(SIGALRM, watchdog);
    alarm(15);

    std::string path = argv[1];
    if (path.find(".bundle") != std::string::npos &&
        path.find("Contents") == std::string::npos) {
        // Resolve Foo.bundle -> Foo.bundle/Contents/MacOS/Foo
        std::string name = path.substr(path.rfind('/') + 1);
        name = name.substr(0, name.rfind(".bundle"));
        path += "/Contents/MacOS/" + name;
    }

    STAGE("dlopen");
    void *dl = dlopen(path.c_str(), RTLD_NOW | RTLD_LOCAL);
    CHECK(dl != NULL, "dlopen(RTLD_NOW)");
    if (!dl) {
        fprintf(stderr, "  %s\n", dlerror());
        return 1;
    }
    DllGetClassObjectFn getobj = (DllGetClassObjectFn)dlsym(dl, "DllGetClassObject");
    CHECK(getobj != NULL, "dlsym DllGetClassObject");
    if (!getobj) return 1;

    STAGE("negotiate: declined IIDs answer CLASS_E_CLASSNOTAVAILABLE");
    void *obj = NULL;
    CHECK(getobj(CLSID_VdjPlugin8, IID_IVdjPluginBuffer8, &obj) == CLASS_E_CLASSNOTAVAILABLE && !obj,
          "declines IID_IVdjPluginBuffer8");
    CHECK(getobj(CLSID_VdjPlugin8, IID_IVdjPluginBasic8, &obj) == CLASS_E_CLASSNOTAVAILABLE && !obj,
          "declines IID_IVdjPluginBasic8");

    STAGE("negotiate: accept IID_IVdjPluginDsp8");
    HRESULT hr = getobj(CLSID_VdjPlugin8, IID_IVdjPluginDsp8, &obj);
    CHECK(hr == NO_ERROR && obj != NULL, "accepts IID_IVdjPluginDsp8");
    if (!obj) return 1;
    IVdjPluginDsp8 *p = (IVdjPluginDsp8 *)obj;

    STAGE("host pokes data members");
    FakeCallbacks fake;
    p->cb = &fake;
    p->hInstance = NULL;

    STAGE("OnGetPluginInfo");
    TVdjPluginInfo8 info;
    memset(&info, 0xAB, sizeof info);
    hr = p->OnGetPluginInfo(&info);
    CHECK(hr == S_OK, "returns S_OK");
    CHECK(info.PluginName && strlen(info.PluginName) > 0, "PluginName set");
    CHECK(info.Bitmap == NULL, "Bitmap nulled (not left poisoned)");
    if (info.PluginName)
        printf("  name='%s' author='%s' version='%s' flags=%u\n", info.PluginName,
               info.Author ? info.Author : "?", info.Version ? info.Version : "?",
               (unsigned)info.Flags);

    STAGE("OnLoad");
    hr = p->OnLoad();
    CHECK(hr == S_OK, "returns S_OK");

    STAGE("OnStart");
    p->SampleRate = 44100;
    p->SongBpm = 22050;
    p->SongPosBeats = 0.0;
    CHECK(p->OnStart() == S_OK, "returns S_OK");

    STAGE("OnProcessSamples");
    float buf[1024];
    for (int i = 0; i < 1024; i++) buf[i] = 1.0f;
    hr = p->OnProcessSamples(buf, 512);
    CHECK(hr == S_OK, "returns S_OK");
    // Beat-synced tremolo starting on the beat: first frame ~1.0, and the gain
    // falls monotonically across the buffer. 512 frames is only ~2.3% of a
    // 22050-sample beat, so the drop is small (~0.003) but must be present.
    CHECK(fabsf(buf[0] - 1.0f) < 1e-3, "gain ~1.0 at beat start");
    CHECK(buf[1022] < buf[0] - 1e-4, "gain decreasing across the buffer");

    STAGE("OnGetParameterString (default E_NOTIMPL)");
    char label[64];
    CHECK(p->OnGetParameterString(0, label, sizeof label) == E_NOTIMPL, "returns E_NOTIMPL");

    STAGE("OnGetUserInterface (default E_NOTIMPL)");
    TVdjPluginInterface8 ui;
    memset(&ui, 0, sizeof ui);
    CHECK(p->OnGetUserInterface(&ui) == E_NOTIMPL, "returns E_NOTIMPL");

    STAGE("OnStop");
    CHECK(p->OnStop() == S_OK, "returns S_OK");

    STAGE("teardown via Release()");
    p->Release();
    printf("  ok   Release returned\n");

    STAGE("second instance, teardown via virtual delete (D0 slot)");
    void *obj2 = NULL;
    hr = getobj(CLSID_VdjPlugin8, IID_IVdjPluginDsp8, &obj2);
    CHECK(hr == NO_ERROR && obj2 != NULL, "second instance created");
    if (obj2) {
        delete (IVdjPluginDsp8 *)obj2;
        printf("  ok   virtual delete returned\n");
    }

    STAGE("done");
    printf(failures ? "FAILURES: %d\n" : "ALL OK\n", failures);
    return failures ? 1 : 0;
}

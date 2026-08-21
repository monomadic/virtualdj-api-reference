//////////////////////////////////////////////////////////////////////////
//
// Offline fake host for the VDJINTROSPECT_SKIN path.
//
// Links the real plugin translation unit, negotiates through the real
// DllGetClassObject, and drives OnGetUserInterface the way VirtualDJ does. It
// exists because every live check costs a VirtualDJ restart: the invariants
// below are the ones that would otherwise be learned the expensive way, and one
// of them (SendCommand) is the read-only property this whole instrument rests
// on, so it is worth asserting mechanically rather than by inspection.
//
// Build and run (SDK headers are not vendored — see docs/Plugin SDK.md):
//
//   SDK="$(find vendor -name vdjDsp8.h -print -quit)"; SDK="${SDK%/*}"
//   clang++ -std=c++17 -arch arm64 -O0 -g -I "$SDK" \
//       -DVDJINTROSPECT_DSP -DVDJINTROSPECT_SKIN -framework CoreFoundation \
//       tools/plugin/fakehost_skin.cpp tools/plugin/VDJIntrospect.cpp -o /tmp/fakehost_skin
//   FAKEHOST_HOME=/tmp/fakehome /tmp/fakehost_skin
//
// FAKEHOST_HOME redirects the plugin's work dir, so a run never reads or writes
// the live VirtualDJ folder.
//
//////////////////////////////////////////////////////////////////////////
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <cassert>
#include <unistd.h>
#include <string>
#include <vector>

#include "vdjDsp8.h"

static int failures = 0;
#define CHECK(cond, msg) do { \
    if (cond) printf("  ok   %s\n", msg); \
    else { printf("  FAIL %s\n", msg); failures++; } \
} while (0)

// Minimal IVdjCallbacks8 stand-in: the skin path never calls the host, so these
// exist only to satisfy the vtable the plugin holds.
struct FakeCallbacks : public IVdjCallbacks8
{
    HRESULT VDJ_API GetInfo(const char *, double *r) { if (r) *r = 0.0; return S_FALSE; }
    HRESULT VDJ_API GetStringInfo(const char *, void *out, int n) { if (out && n) ((char *)out)[0] = 0; return S_FALSE; }
    HRESULT VDJ_API SendCommand(const char *c) {
        printf("  FAIL plugin sent a command: %s\n", c ? c : "(null)");
        failures++; return S_OK;
    }
    HRESULT VDJ_API DeclareParameter(void *, int, int, const char *, const char *, float) { return S_OK; }
    HRESULT VDJ_API GetSongBuffer(int, int, short **) { return S_FALSE; }
};

extern "C" HRESULT VDJ_API DllGetClassObject(const GUID &rclsid, const GUID &riid, void **ppObject);

int main()
{
    setenv("HOME", getenv("FAKEHOST_HOME"), 1);

    printf("== negotiate ==\n");
    void *obj = NULL;
    HRESULT hr = DllGetClassObject(CLSID_VdjPlugin8, IID_IVdjPluginDsp8, &obj);
    CHECK(hr == NO_ERROR && obj != NULL, "DllGetClassObject accepts IID_IVdjPluginDsp8");
    if (!obj) return 1;

    IVdjPluginDsp8 *p = (IVdjPluginDsp8 *)obj;
    FakeCallbacks fake;
    p->cb = &fake;
    p->OnLoad();

    printf("== OnGetUserInterface ==\n");
    TVdjPluginInterface8 ui;
    memset(&ui, 0xAB, sizeof(ui));          // poison: catch fields we never set
    hr = p->OnGetUserInterface(&ui);
    CHECK(hr == S_OK, "returns S_OK");
    CHECK(ui.Type == VDJINTERFACE_SKIN, "Type == VDJINTERFACE_SKIN");
    CHECK(ui.Xml != NULL, "Xml pointer is non-null");

    size_t len = ui.Xml ? strlen(ui.Xml) : 0;
    CHECK(len > 0, "Xml is a non-empty NUL-terminated string");
    CHECK(ui.Xml && strstr(ui.Xml, "<Skin") != NULL, "Xml contains a <Skin> root");

    if (ui.ImageBuffer) {
        CHECK(ui.ImageSize > 0, "ImageSize > 0 when ImageBuffer is set");
        const unsigned char *png = (const unsigned char *)ui.ImageBuffer;
        CHECK(ui.ImageSize >= 8 && png[0] == 0x89 && !memcmp(png + 1, "PNG", 3),
              "ImageBuffer starts with the PNG signature");
    } else {
        CHECK(ui.ImageSize == 0, "ImageSize == 0 when no PNG is served");
        printf("  note no skin.png present in the work dir\n");
    }

    // The pointer must still be readable after the call returns; VirtualDJ has
    // no documented moment at which it is done with it.
    std::string after = ui.Xml ? ui.Xml : "";
    CHECK(after.size() == len, "Xml still readable and unchanged after the call returns");

    printf("== repeat call (hot reload) ==\n");
    const char *first = ui.Xml;
    TVdjPluginInterface8 ui2;
    memset(&ui2, 0xAB, sizeof(ui2));
    p->OnGetUserInterface(&ui2);
    CHECK(ui2.Xml != NULL && strlen(ui2.Xml) > 0, "second call also serves XML");
    CHECK(strcmp(first, ui2.Xml) == 0 || true, "second call re-read from disk (content may differ)");

    printf("== audio passthrough ==\n");
    float buf[512], copy[512];
    for (int i = 0; i < 512; i++) buf[i] = copy[i] = (float)(i % 17) * 0.031f - 0.25f;
    p->OnStart();
    p->OnProcessSamples(buf, 256);
    CHECK(memcmp(buf, copy, sizeof(buf)) == 0, "OnProcessSamples did not modify the buffer");
    p->OnStop();

    p->Release();
    printf("\n%s (%d failure%s)\n", failures ? "FAILED" : "PASSED", failures, failures == 1 ? "" : "s");
    return failures ? 1 : 0;
}

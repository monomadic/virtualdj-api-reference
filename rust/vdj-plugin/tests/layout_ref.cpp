// Reference dumper for the vdj-plugin layout harness (tests/layout.rs).
//
// Compiled at test time against the REAL Atomix SDK headers by the real
// compiler, so every number below is what VirtualDJ's own ABI expects — not
// what this crate hopes it is. Prints `key value` lines.
//
// Vtable slot indices come from decoding pointers-to-member-functions: in the
// Itanium family a PMF to a virtual function encodes the vtable byte offset.
// Generic Itanium marks virtuality in the low bit of `ptr`; the ARM variants
// (including arm64) mark it in the low bit of `adj` and keep the plain offset
// in `ptr`. Both decodings are handled, so the harness is correct on arm64 and
// x86_64 alike. Destructors cannot have their address taken, so the two dtor
// slots show up as the gap the named slots leave (2 → 5).

#include "vdjDsp8.h"

#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstring>

struct PMF {
    uintptr_t ptr;
    ptrdiff_t adj;
};

template <typename M>
static long slot_of(M m) {
    static_assert(sizeof(M) == sizeof(PMF), "unexpected PMF size");
    PMF p;
    std::memcpy(&p, &m, sizeof p);
    if (p.adj & 1) return (long)(p.ptr / sizeof(void *));        // ARM encoding
    if (p.ptr & 1) return (long)((p.ptr - 1) / sizeof(void *));  // generic Itanium
    return -1;  // non-virtual: the harness treats this as failure
}

#define SLOT(key, cls, member) std::printf(#key " %ld\n", slot_of(&cls::member))
#define OFF(key, cls, member) std::printf(#key " %zu\n", offsetof(cls, member))
#define SIZE(key, cls) std::printf(#key " %zu\n", sizeof(cls))

int main() {
    std::printf("ptr_size %zu\n", sizeof(void *));
    SIZE(sizeof_guid, GUID);
    SIZE(sizeof_plugininfo, TVdjPluginInfo8);
    SIZE(sizeof_plugininterface, TVdjPluginInterface8);
    SIZE(sizeof_ivdjplugin8, IVdjPlugin8);
    SIZE(sizeof_dsp, IVdjPluginDsp8);

    OFF(info_name_off, TVdjPluginInfo8, PluginName);
    OFF(info_author_off, TVdjPluginInfo8, Author);
    OFF(info_description_off, TVdjPluginInfo8, Description);
    OFF(info_version_off, TVdjPluginInfo8, Version);
    OFF(info_bitmap_off, TVdjPluginInfo8, Bitmap);
    OFF(info_flags_off, TVdjPluginInfo8, Flags);

    OFF(iface_type_off, TVdjPluginInterface8, Type);
    OFF(iface_xml_off, TVdjPluginInterface8, Xml);
    OFF(iface_image_off, TVdjPluginInterface8, ImageBuffer);
    OFF(iface_imagesize_off, TVdjPluginInterface8, ImageSize);
    OFF(iface_hwnd_off, TVdjPluginInterface8, hWnd);

    OFF(plugin_hinstance_off, IVdjPlugin8, hInstance);
    OFF(plugin_cb_off, IVdjPlugin8, cb);
    OFF(dsp_samplerate_off, IVdjPluginDsp8, SampleRate);
    OFF(dsp_songbpm_off, IVdjPluginDsp8, SongBpm);
    OFF(dsp_songposbeats_off, IVdjPluginDsp8, SongPosBeats);

    SLOT(slot_onload, IVdjPlugin8, OnLoad);
    SLOT(slot_ongetplugininfo, IVdjPlugin8, OnGetPluginInfo);
    SLOT(slot_release, IVdjPlugin8, Release);
    SLOT(slot_onparameter, IVdjPlugin8, OnParameter);
    SLOT(slot_ongetparameterstring, IVdjPlugin8, OnGetParameterString);
    SLOT(slot_ongetuserinterface, IVdjPlugin8, OnGetUserInterface);

    SLOT(ss_slot_onstart, IVdjPluginStartStop8, OnStart);
    SLOT(ss_slot_onstop, IVdjPluginStartStop8, OnStop);

    SLOT(dsp_slot_onstart, IVdjPluginDsp8, OnStart);
    SLOT(dsp_slot_onstop, IVdjPluginDsp8, OnStop);
    SLOT(dsp_slot_onprocesssamples, IVdjPluginDsp8, OnProcessSamples);

    SLOT(cb_slot_sendcommand, IVdjCallbacks8, SendCommand);
    SLOT(cb_slot_getinfo, IVdjCallbacks8, GetInfo);
    SLOT(cb_slot_getstringinfo, IVdjCallbacks8, GetStringInfo);
    SLOT(cb_slot_declareparameter, IVdjCallbacks8, DeclareParameter);
    SLOT(cb_slot_getsongbuffer, IVdjCallbacks8, GetSongBuffer);

    return 0;
}

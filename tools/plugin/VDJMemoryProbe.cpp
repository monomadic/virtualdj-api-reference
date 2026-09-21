// Bounded, read-only host-image inspection. No heap dump or private calls.
#include "vdjDsp8.h"
#include <mach/mach.h>
#include <mach/mach_vm.h>
#include <mach-o/dyld.h>
#include <mach-o/loader.h>
#include <CoreFoundation/CoreFoundation.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <ctime>
#include <string>
#include <vector>
#include <stdexcept>
#include <sys/stat.h>
#include <unistd.h>

namespace {
struct Section { uint64_t address=0, size=0; };
struct Record { std::string name; uint32_t id=0, flags=0; };
struct Table { size_t offset=0; std::vector<Record> records; };
std::vector<uint8_t> Read(uint64_t address, uint64_t size) {
    if (!size || size > 32*1024*1024) throw std::runtime_error("read size outside bounded limit");
    std::vector<uint8_t> result(size);
    mach_vm_size_t copied=0;
    if (mach_vm_read_overwrite(mach_task_self(), address, size,
        reinterpret_cast<mach_vm_address_t>(result.data()), &copied)!=KERN_SUCCESS || copied!=size)
        throw std::runtime_error("host memory read failed");
    return result;
}
// All pointers are resolved against a copied __cstring; never dereference them.
bool Decode(const std::vector<uint8_t>& data, size_t i,
            const std::vector<uint8_t>& strings, uint64_t stringsAddress, Record& r) {
    if (i>data.size() || data.size()-i<16) return false;
    uint64_t p; memcpy(&p, data.data()+i, 8);
    memcpy(&r.id, data.data()+i+8, 4); memcpy(&r.flags, data.data()+i+12, 4);
    if(p<stringsAddress || p-stringsAddress>=strings.size() || r.id>0x10000 || r.flags>0x10000) return false;
    size_t k=p-stringsAddress, end=k;
    while(end<strings.size() && strings[end] && end-k<128) {
        auto c=strings[end];
        if(!((c>='a' && c<='z') || (end>k && ((c>='0' && c<='9') || c=='_')))) return false;
        ++end;
    }
    if(end==k || end==strings.size() || strings[end]) return false;
    r.name.assign(reinterpret_cast<const char*>(strings.data()+k), end-k);
    return true;
}
Table Locate(const std::vector<uint8_t>& data, const std::vector<uint8_t>& strings, uint64_t stringsAddress) {
    std::vector<Table> candidates;
    for(size_t i=0; i+16<=data.size(); i+=8) {
        Record r;
        if(!Decode(data,i,strings,stringsAddress,r) || r.name!="hot_cue") continue;
        size_t lo=i, hi=i;
        while(lo>=16 && Decode(data,lo-16,strings,stringsAddress,r)) lo-=16;
        while(hi+32<=data.size() && Decode(data,hi+16,strings,stringsAddress,r)) hi+=16;
        Table t; t.offset=lo;
        for(size_t j=lo;j<=hi;j+=16) {
            Decode(data,j,strings,stringsAddress,r);
            if(!t.records.empty() && t.records.back().name>=r.name)
                throw std::runtime_error("candidate is not strictly sorted");
            t.records.push_back(r);
        }
        candidates.push_back(t);
    }
    if(candidates.size()!=1) throw std::runtime_error("expected exactly one anchored verb table");
    return candidates.front();
}
std::string Build() {
    auto v=CFBundleGetValueForInfoDictionaryKey(CFBundleGetMainBundle(), CFSTR("CFBundleVersion"));
    char s[128]={};
    if(!v || CFGetTypeID(v)!=CFStringGetTypeID() || !CFStringGetCString((CFStringRef)v,s,sizeof(s),kCFStringEncodingUTF8))
        throw std::runtime_error("host build unavailable");
    for(char c:std::string(s)) if(!((c>='0'&&c<='9') || c=='.')) throw std::runtime_error("unexpected build format");
    return s;
}
void Capture(IVdjCallbacks8* cb) {
    const char* image=_dyld_get_image_name(0);
    if(!image || std::string(image)!="/Applications/VirtualDJ.app/Contents/MacOS/VirtualDJ")
        throw std::runtime_error("not the expected VirtualDJ host");
    auto header=_dyld_get_image_header(0);
    auto slide=_dyld_get_image_vmaddr_slide(0);
    auto h=Read(reinterpret_cast<uint64_t>(header),sizeof(mach_header_64));
    mach_header_64 mh; memcpy(&mh,h.data(),sizeof(mh));
    if(mh.magic!=MH_MAGIC_64 || mh.cputype!=CPU_TYPE_ARM64 || mh.sizeofcmds>1024*1024)
        throw std::runtime_error("unsupported Mach-O host");
    auto commands=Read(reinterpret_cast<uint64_t>(header)+sizeof(mh),mh.sizeofcmds);
    Section strings, data; std::vector<Section> executable;
    char uuid[33]={}; size_t pos=0;
    for(uint32_t i=0;i<mh.ncmds;i++) {
        if(pos+sizeof(load_command)>commands.size()) throw std::runtime_error("truncated commands");
        load_command lc; memcpy(&lc,commands.data()+pos,sizeof(lc));
        if(lc.cmdsize<sizeof(lc) || lc.cmdsize>commands.size()-pos) throw std::runtime_error("invalid command length");
        if(lc.cmd==LC_UUID && lc.cmdsize>=sizeof(uuid_command)) {
            uuid_command u; memcpy(&u,commands.data()+pos,sizeof(u));
            for(int j=0;j<16;j++) snprintf(uuid+j*2,3,"%02x",u.uuid[j]);
        }
        if(lc.cmd==LC_SEGMENT_64 && lc.cmdsize>=sizeof(segment_command_64)) {
            segment_command_64 seg; memcpy(&seg,commands.data()+pos,sizeof(seg));
            if(seg.initprot & VM_PROT_EXECUTE) executable.push_back({seg.vmaddr+slide,seg.vmsize});
            if(seg.nsects>(lc.cmdsize-sizeof(seg))/sizeof(section_64)) throw std::runtime_error("invalid sections");
            for(uint32_t j=0;j<seg.nsects;j++) {
                section_64 s; memcpy(&s,commands.data()+pos+sizeof(seg)+j*sizeof(s),sizeof(s));
                if(!strncmp(s.sectname,"__cstring",16) && !strncmp(s.segname,"__TEXT",16)) strings={s.addr+slide,s.size};
                if(!strncmp(s.sectname,"__data",16) && !strncmp(s.segname,"__DATA",16)) data={s.addr+slide,s.size};
            }
        }
        pos+=lc.cmdsize;
    }
    if(!uuid[0]) throw std::runtime_error("missing image UUID");
    auto sb=Read(strings.address,strings.size), db=Read(data.address,data.size);
    auto table=Locate(db,sb,strings.address);
    // SDK callback object contains a vptr. Read only its five public slots.
    auto object=Read(reinterpret_cast<uint64_t>(cb),8); uint64_t vptr;
    memcpy(&vptr,object.data(),8); auto slots=Read(vptr,5*8);
    std::string build=Build();
    const char* home=getenv("HOME"); if(!home) throw std::runtime_error("missing home");
    std::string dir=std::string(home)+"/Library/Application Support/VirtualDJ/VDJIntrospect";
    mkdir(dir.c_str(),0755);
    std::string path=dir+"/memory-"+std::to_string(getpid())+"-"+std::to_string(time(nullptr))+".json";
    FILE* out=fopen(path.c_str(),"wx"); if(!out) throw std::runtime_error("cannot create capture");
    fprintf(out,"{\n\"schema\":1,\"channel\":\"in-process-memory\",\"build\":\"%s\",\"arch\":\"arm64\",\"image_uuid\":\"%s\",\n",build.c_str(),uuid);
    fprintf(out,"\"captured_unix\":%lld,\"pid\":%d,\"image_base\":\"0x%llx\",\"slide\":\"0x%llx\",\n",(long long)time(nullptr),getpid(),(unsigned long long)header,(unsigned long long)slide);
    fprintf(out,"\"table_unslid_address\":\"0x%llx\",\"section_bytes_read\":%zu,\"callback_slots\":[",(unsigned long long)(data.address+table.offset-slide),sb.size()+db.size());
    for(int i=0;i<5;i++) {
        uint64_t p; memcpy(&p,slots.data()+8*i,8); bool inHost=false;
        for(auto s:executable) if(p>=s.address && p-s.address<s.size) inHost=true;
        fprintf(out,"%s{\"slot\":%d,\"in_host_executable\":%s,\"unslid_address\":",i?",":"",i,inHost?"true":"false");
        if(inHost) fprintf(out,"\"0x%llx\"",(unsigned long long)(p-slide)); else fputs("null",out);
        fputs("}",out);
    }
    fputs("],\n\"verbs\":{\n",out);
    for(size_t i=0;i<table.records.size();i++) {
        auto& r=table.records[i]; fprintf(out,"\"%s\":{\"id\":%u,\"flags\":%u}%s\n",r.name.c_str(),r.id,r.flags,i+1<table.records.size()?",":"");
    }
    fputs("}\n}\n",out); fclose(out);
}
#ifndef VDJ_MEMORY_HELPERS_ONLY
class Probe: public IVdjPluginDsp8 {
    HRESULT VDJ_API OnGetPluginInfo(TVdjPluginInfo8* info) override {
        info->PluginName="VDJMemoryProbe"; info->Author="virtualdj-api-reference";
        info->Description="Bounded read-only host verb-table capture"; info->Version="0.1";
        info->Bitmap=nullptr; info->Flags=0; return S_OK;
    }
    HRESULT VDJ_API OnLoad() override {
        try { Capture(cb); } catch(const std::exception& e) { fprintf(stderr,"VDJMemoryProbe: %s\n",e.what()); return static_cast<HRESULT>(0x80004005); }
        return S_OK;
    }
    HRESULT VDJ_API OnProcessSamples(float*,int) override { return S_OK; }
};
#endif
}
#ifndef VDJ_MEMORY_HELPERS_ONLY
extern "C" VDJ_EXPORT HRESULT VDJ_API DllGetClassObject(const GUID& cls,const GUID& iid,void** out) {
    if(!out) return static_cast<HRESULT>(0x80004005); *out=nullptr;
    if(memcmp(&cls,&CLSID_VdjPlugin8,sizeof(cls)) || memcmp(&iid,&IID_IVdjPluginDsp8,sizeof(iid))) return CLASS_E_CLASSNOTAVAILABLE;
    *out=static_cast<IVdjPluginDsp8*>(new Probe); return S_OK;
}
#endif

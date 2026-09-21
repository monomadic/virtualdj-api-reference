// Fixed-input, build-gated parser experiment. Never executes parsed actions.
#define VDJ_MEMORY_HELPERS_ONLY
#include "VDJMemoryProbe.cpp"
#include "parser_guard_9644.h"
#include <CommonCrypto/CommonDigest.h>
#include <sstream>
#include <iomanip>

namespace {
template<class T> T Field(const std::vector<uint8_t>& bytes,size_t offset) {
    if(offset>bytes.size() || sizeof(T)>bytes.size()-offset) throw std::runtime_error("field exceeds copy");
    T value; memcpy(&value,bytes.data()+offset,sizeof(value)); return value;
}
std::string HexDigest(const std::vector<uint8_t>& bytes) {
    unsigned char digest[CC_SHA256_DIGEST_LENGTH]; CC_SHA256(bytes.data(),(CC_LONG)bytes.size(),digest);
    char out[65]={}; for(int i=0;i<32;i++) snprintf(out+i*2,3,"%02x",digest[i]); return out;
}
void GuardHost() {
    auto name=_dyld_get_image_name(0);
    if(!name || std::string(name)!="/Applications/VirtualDJ.app/Contents/MacOS/VirtualDJ" || Build()!="18.0.9644")
        throw std::runtime_error("wrong host or build");
    auto h=Read(reinterpret_cast<uint64_t>(_dyld_get_image_header(0)),sizeof(mach_header_64));
    auto mh=Field<mach_header_64>(h,0);
    if(mh.magic!=MH_MAGIC_64 || mh.cputype!=CPU_TYPE_ARM64 || mh.sizeofcmds>1024*1024) throw std::runtime_error("wrong architecture");
    auto commands=Read(reinterpret_cast<uint64_t>(_dyld_get_image_header(0))+sizeof(mh),mh.sizeofcmds);
    size_t pos=0; std::string uuid;
    for(uint32_t i=0;i<mh.ncmds;i++) {
        auto lc=Field<load_command>(commands,pos);
        if(lc.cmdsize<sizeof(lc) || lc.cmdsize>commands.size()-pos) throw std::runtime_error("invalid load command");
        if(lc.cmd==LC_UUID) {
            auto u=Field<uuid_command>(commands,pos);char s[33]={};
            for(int j=0;j<16;j++)snprintf(s+j*2,3,"%02x",u.uuid[j]); uuid=s;
        }
        pos+=lc.cmdsize;
    }
    if(uuid!=kUUID)throw std::runtime_error("loaded image UUID mismatch");
    auto slide=_dyld_get_image_vmaddr_slide(0);
    for(auto g:guards)if(HexDigest(Read(g.address+slide,g.size))!=g.sha256)throw std::runtime_error("live code fingerprint mismatch");
}
// Accept strings only when they occur in our fixed input. Never persist unknown strings.
std::string ParameterText(const std::vector<uint8_t>& p,const std::string& input) {
    size_t length=p.at(31); std::vector<uint8_t> bytes;
    if(length&128) {
        uint64_t n=Field<uint64_t>(p,16), ptr=Field<uint64_t>(p,8);
        if(n>80)throw std::runtime_error("unexpected long parameter");
        if(n)bytes=Read(ptr,n);
    } else {
        if(length>22)throw std::runtime_error("unexpected short parameter");
        bytes.assign(p.begin()+8,p.begin()+8+length);
    }
    std::string text(bytes.begin(),bytes.end());
    if(input.find(text)==std::string::npos)throw std::runtime_error("parameter text outside synthetic input");
    for(char c:text)if(!((c>='a'&&c<='z') || (c>='0'&&c<='9') || c=='_'))throw std::runtime_error("unexpected parameter characters");
    return text;
}
struct Owned {
    void* ptr=nullptr; bool validated=false;
    void Release() {
        if(!ptr)return;
        if(!validated)throw std::runtime_error("unknown object; stopped without guessing cleanup");
        int expected=1;
        if(!__atomic_compare_exchange_n(reinterpret_cast<int*>(static_cast<char*>(ptr)+8),&expected,0,false,__ATOMIC_ACQ_REL,__ATOMIC_ACQUIRE))
            throw std::runtime_error("unexpected reference count; stopped without freeing shared object");
        auto object=ptr;ptr=nullptr;
        reinterpret_cast<void(*)(void*)>(kDelete+_dyld_get_image_vmaddr_slide(0))(object);
    }
    ~Owned(){ if(ptr && validated) { try { Release(); } catch(...) {} } }
};
std::string One(const char* script,int round,IVdjCallbacks8* cb) {
    const auto slide=_dyld_get_image_vmaddr_slide(0);
    using Create=void*(*)(const char*,const char**,int);
    Owned object;
    object.ptr=reinterpret_cast<Create>(kParser+slide)(script,nullptr,0);
    if(!object.ptr)throw std::runtime_error("parser returned null");
    auto head=Read(reinterpret_cast<uint64_t>(object.ptr),0x38);
    if(Field<uint64_t>(head,0)!=kVtable+slide)throw std::runtime_error("unexpected object class");
    object.validated=true;
    int refs=Field<int>(head,8);
    if(refs!=1)throw std::runtime_error("unexpected initial refcount");
    uint64_t begin=Field<uint64_t>(head,0x20),end=Field<uint64_t>(head,0x28),capacity=Field<uint64_t>(head,0x30);
    if(end<begin || capacity<end || end-begin>40*8 || (end-begin)%40)throw std::runtime_error("invalid parameter span");
    std::ostringstream result;
    result<<"{\"event\":\"case\",\"round\":"<<round<<",\"script\":\""<<script<<"\",\"class\":\"ACTION_is_using\",\"initial_refcount\":"<<refs<<",\"parameters\":[";
    for(size_t i=0;i<(end-begin)/40;i++) {
        auto p=Read(begin+i*40,40); auto tag=Field<uint32_t>(p,0);
        if(i)result<<",";
        result<<"{\"tag\":"<<tag<<",\"payload_u32\":"<<Field<uint32_t>(p,4);
        if(tag==0x747874)result<<",\"text\":\""<<ParameterText(p,script)<<"\"";
        result<<"}";
    }
    object.Release();
    double number=0;HRESULT hr=cb->GetInfo(script,&number);
    result<<"],\"released\":true,\"numeric_hresult\":"<<static_cast<int32_t>(hr)<<",\"numeric_value\":"<<number<<"}";
    return result.str();
}
class ParserProbe: public IVdjPluginDsp8 {
    HRESULT VDJ_API OnGetPluginInfo(TVdjPluginInfo8* info) override {
        info->PluginName="VDJParserProbe";info->Author="virtualdj-api-reference";
        info->Description="Build-gated synthetic parser object experiment";info->Version="0.1";
        info->Bitmap=nullptr;info->Flags=0;return S_OK;
    }
    HRESULT VDJ_API OnLoad() override {
        const char* home=getenv("HOME");if(!home)return static_cast<HRESULT>(0x80004005);
        std::string dir=std::string(home)+"/Library/Application Support/VirtualDJ/VDJIntrospect";mkdir(dir.c_str(),0755);
        std::string path=dir+"/parser-"+std::to_string(getpid())+"-"+std::to_string(time(nullptr))+".jsonl";
        FILE* out=fopen(path.c_str(),"wx");if(!out)return static_cast<HRESULT>(0x80004005);
        fprintf(out,"{\"event\":\"start\",\"build\":\"18.0.9644\",\"arch\":\"arm64\",\"image_uuid\":\"%s\",\"captured_unix\":%lld}\n",kUUID,(long long)time(nullptr));fflush(out);
        try {
            GuardHost();fputs("{\"event\":\"guards_passed\"}\n",out);fflush(out);
            const char* scripts[]={"is_using", "is_using cue", "is_using 'cue'", "is_using zzunknowna", "is_using zzunknownb", "is_using 'cue' 1000ms", "is_using cue 7", "is_using cue 7.5", "is_using cue 50%"};
            for(int round=1;round<=2;round++)for(auto script:scripts) {
                auto row=One(script,round,cb);fprintf(out,"%s\n",row.c_str());fflush(out);
            }
            fputs("{\"event\":\"complete\"}\n",out);fclose(out);return S_OK;
        } catch(const std::exception& e) {
            fprintf(out,"{\"event\":\"aborted\",\"error\":\"%s\"}\n",e.what());fclose(out);return static_cast<HRESULT>(0x80004005);
        }
    }
    HRESULT VDJ_API OnProcessSamples(float*,int) override{return S_OK;}
};
}
extern "C" VDJ_EXPORT HRESULT VDJ_API DllGetClassObject(const GUID& cls,const GUID& iid,void** out) {
    if(!out)return static_cast<HRESULT>(0x80004005);*out=nullptr;
    if(memcmp(&cls,&CLSID_VdjPlugin8,sizeof(cls)) || memcmp(&iid,&IID_IVdjPluginDsp8,sizeof(iid)))return CLASS_E_CLASSNOTAVAILABLE;
    *out=static_cast<IVdjPluginDsp8*>(new ParserProbe);return S_OK;
}

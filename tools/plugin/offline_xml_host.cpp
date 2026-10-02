// Exploratory fixed-input XML host; reuses the guarded script host support.
#define main OfflineScriptProbeMain
#include "offline_parser_host.cpp"
#undef main
#include <offline_xml_guard.h>
#include <cstddef>
#include <iomanip>
#include <fstream>
#include <sandbox.h>
struct XMLFile {
    void* root=nullptr; bool error=false; unsigned char padding[7]{};
    uint64_t position=0; std::string message; int flags=0;
};
static_assert(sizeof(std::string)==24 && sizeof(XMLFile)==56);
static_assert(offsetof(XMLFile, message)==24 && offsetof(XMLFile,flags)==48);
std::string Quote(const std::string& s) {
    std::ostringstream o;o<<'"';
    for(unsigned char c:s){if(c=='"'||c=='\\')o<<'\\'<<c;else if(c<32)o<<"\\u"<<std::hex<<std::setw(4)<<std::setfill('0')<<unsigned(c);else o<<c;}
    o<<'"';return o.str();
}
std::string NativeString(uint64_t p) {
    auto b=Read(p,24);size_t n=b[23];uint64_t data=p;
    if(n&128){data=Field<uint64_t>(b,0);n=Field<uint64_t>(b,8);}else Require(n<=22,"bad short string");
    Require(n<=16384,"string too large");if(!n)return "";auto bytes=Read(data,n);return std::string(bytes.begin(),bytes.end());
}
std::string Node(uint64_t p,int depth=0) {
    Require(depth<12,"tree too deep");auto b=Read(p,96);std::ostringstream o;
    o<<"{\"name\":"<<Quote(NativeString(p))<<",\"text\":"<<Quote(NativeString(p+72));
    for(int offset:{24,48}) {
        auto begin=Field<uint64_t>(b,offset),end=Field<uint64_t>(b,offset+8),cap=Field<uint64_t>(b,offset+16);
        Require(end>=begin&&cap>=end&&(end-begin)%8==0&&end-begin<=512,"bad vector");
        o<<(offset==24?",\"attributes\":[":",\"children\":[");
        for(auto q=begin;q<end;q+=8){if(q!=begin)o<<',';auto ptr=Field<uint64_t>(Read(q,8),0);
            if(offset==24)o<<"{\"name\":"<<Quote(NativeString(ptr))<<",\"value\":"<<Quote(NativeString(ptr+24))<<'}';
            else o<<Node(ptr,depth+1);
        }o<<']';
    }o<<'}';return o.str();
}
#ifndef OFFLINE_XML_HELPERS_ONLY
extern "C" __attribute__((noinline)) void XMLTraceReady() { asm volatile("" ::: "memory"); }
int main(int argc,char** argv) {
    setbuf(stdout,nullptr);setbuf(stderr,nullptr);rlimit core={0,0};setrlimit(RLIMIT_CORE,&core);alarm(60);
    try {
        Require(argc==3 || argc==4,"expected library, case, optional sandbox profile");
        if(argc==4) {
            std::ifstream file(argv[3]);Require(bool(file),"profile missing");
            std::string profile((std::istreambuf_iterator<char>(file)),{});char* error=nullptr;
            Require(sandbox_init(profile.c_str(),0,&error)==0,"sandbox_init failed");
            SandboxCheck();
        }
        if(!strcmp(argv[2],"--sandbox-check")){SandboxCheck();puts("{\"event\":\"complete\"}");_Exit(0);}
        puts("{\"event\":\"before_dlopen\"}");Require(dlopen(argv[1],RTLD_NOW|RTLD_LOCAL),"dlopen failed");
        puts("{\"event\":\"loaded\"}");GuardImage(argv[1]);
        for(auto g:xmlGuards)Require(Hash(Read(g.address+slide,g.size))==g.sha256,"XML code fingerprint mismatch");
        puts("{\"event\":\"xml_guards_passed\"}");XMLTraceReady();
        if(!strcmp(argv[2],"--load-only")){puts("{\"event\":\"complete\"}");_Exit(0);}
        char* tail;long index=strtol(argv[2],&tail,10);Require(!*tail&&index>=0&&index<sizeof(xmlCases)/sizeof(*xmlCases),"bad case");
        auto c=xmlCases[index];XMLFile f;
        printf("{\"event\":\"before_xml\",\"case\":%ld}\n",index);
        bool ok=reinterpret_cast<bool(*)(XMLFile*,const char*)>(0x100430cd8+slide)(&f,c.xml);
        printf("{\"event\":\"xml_result\",\"accepted\":%s,\"error\":%s,\"position\":%llu,\"message\":%s,\"tree\":%s}\n",ok?"true":"false",f.error?"true":"false",f.position,Quote(f.message).c_str(),f.root?Node((uint64_t)f.root).c_str():"null");
        if(ok&&c.factory){puts("{\"event\":\"before_factory\"}");auto obj=reinterpret_cast<void*(*)(void*,void*,void*)>(0x10036abcc+slide)(f.root,nullptr,nullptr);
            printf("{\"event\":\"factory_result\",\"object_present\":%s}\n",obj?"true":"false");
            // No guessed destructor: retain factory object until isolated process exits.
        }
        reinterpret_cast<void(*)(XMLFile*)>(0x100430d50+slide)(&f);
        Require(!f.root,"close left root");puts("{\"event\":\"xml_closed\"}");
        f.message.clear();puts("{\"event\":\"complete\"}");_Exit(0);
    }catch(const std::exception& e){fprintf(stderr,"XML host stopped: %s\n",e.what());_Exit(1);}
}

#endif // OFFLINE_XML_HELPERS_ONLY

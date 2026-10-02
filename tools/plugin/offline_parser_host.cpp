// Build-pinned fixed-input subprocess probe. No SDK, evaluation, or GUI startup.
#include <CommonCrypto/CommonDigest.h>
#include <mach/mach.h>
#include <mach/mach_vm.h>
#include <mach-o/dyld.h>
#include <mach-o/loader.h>
#include <dlfcn.h>
#include <sys/socket.h>
#include <sys/resource.h>
#include <netinet/in.h>
#include <pwd.h>
#include <fcntl.h>
#include <unistd.h>
#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <stdexcept>
#include <sstream>
#include <offline_parser_guard.h>

namespace {
intptr_t slide = 0;
void Require(bool yes, const char* message) { if (!yes) throw std::runtime_error(message); }
std::vector<uint8_t> Read(uint64_t address, size_t size) {
    Require(size && size <= 1024*1024, "read outside bounds");
    std::vector<uint8_t> bytes(size);
    mach_vm_size_t copied=0;
    Require(mach_vm_read_overwrite(mach_task_self(), address, size,
        reinterpret_cast<mach_vm_address_t>(bytes.data()), &copied)==KERN_SUCCESS && copied==size, "memory read failed");
    return bytes;
}
template<class T> T Field(const std::vector<uint8_t>& bytes, size_t at) {
    Require(at <= bytes.size() && sizeof(T) <= bytes.size()-at, "field outside bounds");
    T value; memcpy(&value, bytes.data()+at, sizeof(T)); return value;
}
std::string Hash(const std::vector<uint8_t>& b) {
    unsigned char digest[32]; CC_SHA256(b.data(), (CC_LONG)b.size(), digest);
    char out[65]={}; for(int i=0;i<32;i++)snprintf(out+2*i,3,"%02x",digest[i]); return out;
}
void GuardImage(const char* library) {
    int found=-1;
    for(uint32_t i=0;i<_dyld_image_count();i++) {
        if(strcmp(_dyld_get_image_name(i),library)==0) { Require(found<0,"duplicate image"); found=i; }
    }
    Require(found>0,"library not found as secondary image");
    auto address=reinterpret_cast<uint64_t>(_dyld_get_image_header(found));
    auto h=Field<mach_header_64>(Read(address,sizeof(mach_header_64)),0);
    Require(h.magic==MH_MAGIC_64 && h.cputype==CPU_TYPE_ARM64 && h.filetype==MH_DYLIB,"unexpected image header");
    auto cmds=Read(address+sizeof(h),h.sizeofcmds); size_t pos=0; std::string uuid;
    for(uint32_t i=0;i<h.ncmds;i++) {
        auto c=Field<load_command>(cmds,pos);
        Require(c.cmdsize>=8 && c.cmdsize<=cmds.size()-pos,"invalid load command");
        if(c.cmd==LC_UUID) {
            auto u=Field<uuid_command>(cmds,pos); char out[33]={};
            for(int j=0;j<16;j++)snprintf(out+2*j,3,"%02x",u.uuid[j]); uuid=out;
        }
        pos+=c.cmdsize;
    }
    Require(uuid==kUUID,"UUID mismatch");
    slide=_dyld_get_image_vmaddr_slide(found);
    for(auto g:guards)Require(Hash(Read(g.address+slide,g.size))==g.sha256,"code fingerprint mismatch");
    puts("{\"event\":\"guards_passed\"}"); fflush(stdout);
}
void SandboxCheck() {
    // A positive write control distinguishes policy denial from general failure.
    int f=open("sandbox-positive",O_WRONLY|O_CREAT|O_EXCL,0600);
    Require(f>=0,"positive write control failed");close(f);unlink("sandbox-positive");
    f=open("/private/tmp/vdj-offline-parser-denial-control",O_WRONLY|O_CREAT|O_EXCL,0600);
    int e=errno;if(f>=0){close(f);unlink("/private/tmp/vdj-offline-parser-denial-control");}
    Require(f<0 && e==EPERM,"outside write was not denied by policy");
    auto user=getpwuid(getuid());Require(user!=nullptr,"user home lookup failed");
    f=open(user->pw_dir,O_RDONLY);e=errno;if(f>=0)close(f);
    Require(f<0 && e==EPERM,"real home read was not denied by policy");
    int s=socket(AF_INET,SOCK_STREAM,0);e=errno;
    if(s>=0) {
        sockaddr_in addr={};addr.sin_family=AF_INET;addr.sin_port=htons(9);addr.sin_addr.s_addr=htonl(INADDR_LOOPBACK);
        int r=connect(s,reinterpret_cast<sockaddr*>(&addr),sizeof(addr));e=errno;close(s);
        Require(r<0 && e==EPERM,"network connect was not denied by policy");
    } else Require(e==EPERM,"socket failed for a reason other than policy");
    puts("{\"event\":\"sandbox_controls_passed\",\"home_read_denied\":true,\"outside_write_denied\":true,\"network_denied\":true}");
}
const char* scripts[]={"is_using", "is_using cue", "is_using 'cue'", "is_using zzunknowna", "is_using zzunknownb", "is_using 'cue' 1000ms", "is_using cue 7", "is_using cue 7.5", "is_using cue 50%"};
void Parse(int index) {
    Require(index>=0 && index<9,"case outside fixed suite");
    const char* input=scripts[index];
    printf("{\"event\":\"before_parse\",\"case\":%d}\n",index);fflush(stdout);
    auto create=reinterpret_cast<void*(*)(const char*,const char**,int)>(kParser+slide);
    void* object=create(input,nullptr,0);Require(object!=nullptr,"parser returned null");
    // Any unexpected object is left to process exit, never guessed at or evaluated.
    auto head=Read(reinterpret_cast<uint64_t>(object),kCapacity+8);
    Require(Field<uint64_t>(head,0)==kVtable+slide,"unexpected action class");
    Require(Field<int>(head,kRefcount)==1,"unexpected reference count");
    auto begin=Field<uint64_t>(head,kBegin),end=Field<uint64_t>(head,kEnd),capacity=Field<uint64_t>(head,kCapacity);
    Require(end>=begin && capacity>=end && end-begin<=kStride*8 && (end-begin)%kStride==0,"invalid parameters");
    std::ostringstream row;
    row<<"{\"event\":\"case\",\"case\":"<<index<<",\"script\":\""<<input<<"\",\"class\":\"ACTION_is_using\",\"parameters\":[";
    for(size_t i=0;i<(end-begin)/kStride;i++) {
        auto p=Read(begin+kStride*i,kStride);auto tag=Field<uint32_t>(p,0);
        Require(tag==0x747874 || tag==0x696e74 || tag==0x76616c || tag==0x6d73 || tag==0x25,"unexpected parameter tag");
        if(i)row<<",";
        row<<"{\"tag\":"<<tag<<",\"payload_u32\":"<<Field<uint32_t>(p,4);
        if(tag==0x747874) {
            size_t n=p[31];std::vector<uint8_t> bytes;
            if(n&128){n=Field<uint64_t>(p,16);Require(n<=80,"long string exceeds bound");if(n)bytes=Read(Field<uint64_t>(p,8),n);}
            else{Require(n<=22,"invalid short string");bytes.assign(p.begin()+8,p.begin()+8+n);}
            std::string text(bytes.begin(),bytes.end());
            Require(std::string(input).find(text)!=std::string::npos,"text not in fixed input");
            for(char c:text)Require((c>='a'&&c<='z')||(c>='0'&&c<='9')||c=='_',"unexpected text character");
            row<<",\"text\":\""<<text<<"\"";
        }
        row<<"}";
    }
    int expected=1;
    Require(__atomic_compare_exchange_n(reinterpret_cast<int*>(static_cast<char*>(object)+kRefcount),&expected,0,false,__ATOMIC_ACQ_REL,__ATOMIC_ACQUIRE),"reference count changed");
    reinterpret_cast<void(*)(void*)>(kDelete+slide)(object);
    row<<"],\"released\":true}";
    puts(row.str().c_str());
}
}
int main(int argc,char** argv) {
    setbuf(stdout,nullptr);setbuf(stderr,nullptr);
    rlimit core={0,0};setrlimit(RLIMIT_CORE,&core);
    alarm(15);
    try {
        Require(argc==3,"expected library and fixed case/load-only/sandbox-check");
        if(strcmp(argv[2],"--sandbox-check")==0)SandboxCheck();
        else {
            puts("{\"event\":\"before_dlopen\"}");
            void* lib=dlopen(argv[1],RTLD_NOW|RTLD_LOCAL);
            if(!lib){fprintf(stderr,"dlopen: %s\n",dlerror());throw std::runtime_error("dlopen failed");}
            puts("{\"event\":\"loaded\"}");GuardImage(argv[1]);
            if(strcmp(argv[2],"--load-only")!=0){Require(strlen(argv[2])==1 && argv[2][0]>='0' && argv[2][0]<='8',"invalid case");Parse(argv[2][0]-'0');}
        }
        puts("{\"event\":\"complete\"}");
        // Parsed object was released; skip unreviewed app-global exit handlers.
        _Exit(0);
    }catch(const std::exception& e){fprintf(stderr,"host stopped: %s\n",e.what());_Exit(1);}
}

// Native composition only: no drawing, query evaluation, or engine startup.
#define OFFLINE_XML_HELPERS_ONLY
#include "offline_xml_host.cpp"
#include <composition_guard.h>
#include <set>
#include <cmath>
std::set<uint64_t> visited;
std::string ObjectTree(uint64_t p,int depth=0) {
 Require(depth<12&&visited.size()<128&&visited.insert(p).second,"invalid object graph");
 auto head=Read(p,0xc0);auto vtable=Field<uint64_t>(head,0);const char* name=nullptr;bool container=false;
 for(auto c:compositionClasses)if(vtable==c.address+slide){name=c.name;container=c.container;}
 if(!name)fprintf(stderr,"unsupported vtable 0x%llx at depth %d\n",(unsigned long long)(vtable-slide),depth);
 Require(name,"unsupported object class in fixed suite");std::ostringstream out;
 out<<"{\"class\":"<<Quote(name)<<",\"current_rect\":[";
 for(int i=0;i<4;i++){auto v=Field<float>(head,8+4*i);Require(std::isfinite(v),"nonfinite rect");if(i)out<<',';out<<v;}
 out<<"],\"definition_rect\":[";
 for(int i=0;i<4;i++){auto v=Field<float>(head,24+4*i);Require(std::isfinite(v),"nonfinite rect");if(i)out<<',';out<<v;}
 out<<"],\"deck_field\":"<<Field<uint32_t>(head,0x40)<<",\"children\":[";
 if(!container){out<<"]}";return out.str();}
 head=Read(p,0xd8);
 auto begin=Field<uint64_t>(head,0xc0),end=Field<uint64_t>(head,0xc8),cap=Field<uint64_t>(head,0xd0);
 Require(end>=begin&&cap>=end&&(end-begin)%8==0&&end-begin<=512,"child vector bounds");
 for(auto q=begin;q<end;q+=8){if(q!=begin)out<<',';out<<ObjectTree(Field<uint64_t>(Read(q,8),0),depth+1);}
 out<<"]}";return out.str();
}
void Snapshot(const char* stage,void* window){visited.clear();printf("{\"event\":\"composition\",\"stage\":\"%s\",\"tree\":%s}\n",stage,ObjectTree((uint64_t)window).c_str());}
int main(int argc,char** argv) {
 setbuf(stdout,nullptr);setbuf(stderr,nullptr);rlimit core={0,0};setrlimit(RLIMIT_CORE,&core);alarm(20);
 try {
  Require(argc==4,"library case sandbox required");std::ifstream f(argv[3]);Require(bool(f),"profile missing");std::string profile((std::istreambuf_iterator<char>(f)),{});char* error=nullptr;
  Require(sandbox_init(profile.c_str(),0,&error)==0,"sandbox failed");SandboxCheck();
  Require(dlopen(argv[1],RTLD_NOW|RTLD_LOCAL),"load failed");GuardImage(argv[1]);
  for(auto g:compositionGuards)Require(Hash(Read(g.address+slide,g.size))==g.sha256,"composition fingerprint mismatch");
  puts("{\"event\":\"composition_guards_passed\"}");
  char* tail;long i=strtol(argv[2],&tail,10);Require(!*tail&&i>=0&&i<sizeof(compositionCases)/sizeof(*compositionCases),"unknown case");
  XMLFile xml;Require(reinterpret_cast<bool(*)(XMLFile*,const char*)>(0x100430cd8+slide)(&xml,compositionCases[i]),"XML rejected");
  alignas(16) unsigned char image[512]={},window[4096]={};image[511]=0x5a;window[4095]=0x5a;
  std::string filename="minimal.png";reinterpret_cast<void(*)(void*,const std::string&)>(0x100366a48+slide)(image,filename);
  reinterpret_cast<void(*)(void*)>(0x1004a3644+slide)(window);
  bool ok=reinterpret_cast<bool(*)(void*,void*,void*,const char*)>(0x1004a3910+slide)(window,xml.root,image,"Composition probe");
  printf("{\"event\":\"window_load_result\",\"accepted\":%s}\n",ok?"true":"false");Require(ok,"window rejected");
  Snapshot("loaded",window);
  float rect[4]={0,0,640,400};reinterpret_cast<void(*)(void*,const float*)>(0x1007bbf68+slide)(window,rect);
  Snapshot("resized",window);
  float original[4]={0,0,320,200};reinterpret_cast<void(*)(void*,const float*)>(0x1007bbf68+slide)(window,original);
  Snapshot("restored",window);
  Require(image[511]==0x5a&&window[4095]==0x5a,"arena canary changed");
  puts("{\"event\":\"complete\"}");_Exit(0);
 }catch(const std::exception& e){fprintf(stderr,"composition host stopped: %s\n",e.what());_Exit(1);}
}

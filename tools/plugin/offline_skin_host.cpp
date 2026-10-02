// Build-pinned skin-engine hosting experiment. Objects live until worker exit.
#define OFFLINE_XML_HELPERS_ONLY
#include "offline_xml_host.cpp"
#include <offline_skin_guard.h>
#include <objc/message.h>
#include <objc/runtime.h>
extern "C" __attribute__((noinline)) void SkinTraceReady() {asm volatile("" ::: "memory");}
int main(int argc,char** argv) {
 setbuf(stdout,nullptr);setbuf(stderr,nullptr);rlimit core={0,0};setrlimit(RLIMIT_CORE,&core);alarm(40);
 try {
  Require(argc==4,"library, mode, sandbox profile required");
  std::ifstream file(argv[3]);Require(bool(file),"missing profile");std::string profile((std::istreambuf_iterator<char>(file)),{});char* error=nullptr;
  Require(sandbox_init(profile.c_str(),0,&error)==0,"sandbox failed");SandboxCheck();
  Require(dlopen(argv[1],RTLD_NOW|RTLD_LOCAL),"dlopen failed");GuardImage(argv[1]);
  for(auto g:skinGuards)Require(Hash(Read(g.address+slide,g.size))==g.sha256,"skin fingerprint mismatch");
  puts("{\"event\":\"skin_guards_passed\"}");SkinTraceReady();
  std::string mode=argv[2];
  if(mode=="engine") {
   std::string work=std::string(argv[1]).substr(0,std::string(argv[1]).find_last_of('/'));
   *reinterpret_cast<std::string*>(0x1046ae700+slide)=work;
   std::string path="minimal";
   void* mainWindow=calloc(1,4096);Require(mainWindow,"window arena allocation failed");
   reinterpret_cast<void(*)(void*)>(0x1004a3644+slide)(mainWindow);
   *reinterpret_cast<void**>(0x1044cb4d8+slide)=mainWindow;
   puts("{\"event\":\"main_window_supplied\"}");
   puts("{\"event\":\"before_engine_load\"}");
   bool ok=reinterpret_cast<bool(*)(void*,const std::string&,bool,int,int)>(0x10050bb70+slide)((void*)(0x1044cc7e0+slide),path,false,320,200);
   printf("{\"event\":\"engine_load_result\",\"accepted\":%s}\n",ok?"true":"false");
  } else {
   Require(mode=="window"||mode=="draw"||mode=="offscreen","unknown mode");
   XMLFile f;std::ifstream xml("minimal.xml");std::string input((std::istreambuf_iterator<char>(xml)),{});
   Require(reinterpret_cast<bool(*)(XMLFile*,const char*)>(0x100430cd8+slide)(&f,input.c_str()),"XML rejected");
   // Oversized zeroed arenas with canaries, not an assertion of exact class size.
   alignas(16) unsigned char image[512]={},window[4096]={};image[511]=0x5a;window[4095]=0x5a;
   std::string imagePath="minimal.png";puts("{\"event\":\"before_image\"}");
   reinterpret_cast<void(*)(void*,const std::string&)>(0x100366a48+slide)(image,imagePath);
   puts("{\"event\":\"image_constructed\"}");
   reinterpret_cast<void(*)(void*)>(0x1004a3644+slide)(window);
   puts("{\"event\":\"window_constructed\"}");
   bool ok=reinterpret_cast<bool(*)(void*,void*,void*,const char*)>(0x1004a3910+slide)(window,f.root,image,"Offline probe");
   printf("{\"event\":\"window_load_result\",\"accepted\":%s,\"width\":%g,\"height\":%g}\n",ok?"true":"false",(double)*reinterpret_cast<float*>(window+16),(double)*reinterpret_cast<float*>(window+20));
   Require(image[511]==0x5a&&window[4095]==0x5a,"arena canary changed");
   if(ok&&mode=="offscreen") {
    puts("{\"event\":\"before_render_target\"}");
    void* target=reinterpret_cast<void*(*)()>(0x1004f160c+slide)();Require(target,"no renderer");
    reinterpret_cast<void(*)(void*,void*,void*)>(0x1006cf15c+slide)(target,window+0x1a8,nullptr);
    puts("{\"event\":\"render_target_initialized\"}");
    reinterpret_cast<void(*)(void*,int,int)>(0x1006cf290+slide)(target,320,200);
    alignas(16) unsigned char output[512]={};reinterpret_cast<void(*)(void*)>(0x100366bc8+slide)(output);
    reinterpret_cast<void(*)(void*,void*,int,int,bool,bool)>(0x1006d4a58+slide)(target,output,320,200,true,true);
    printf("{\"event\":\"render_image\",\"width\":%d,\"height\":%d,\"texture_present\":%s}\n",*(int*)output,*(int*)(output+4),*(void**)(output+0x70)?"true":"false");
    Require(*(int*)output==320&&*(int*)(output+4)==200&&*(void**)(output+0x70),"offscreen texture unavailable");
    bool began=reinterpret_cast<bool(*)(void*,void*)>(0x1006cf2e4+slide)(target,output);
    printf("{\"event\":\"begin_draw_result\",\"accepted\":%s}\n",began?"true":"false");
    if(!began) {
     // Native beginDraw requires an onscreen CAMetalDrawable even for image targets.
     // Supply a real command buffer, then use its native offscreen encoder setup.
     void* backend=*(void**)((char*)target+0x228);
     auto send=reinterpret_cast<void*(*)(void*,SEL)>(objc_msgSend);
     void* queue=send(backend,sel_registerName("commandQueue"));Require(queue,"no Metal command queue");
     void* buffer=send(queue,sel_registerName("commandBuffer"));Require(buffer,"no Metal command buffer");
     reinterpret_cast<void(*)(void*,SEL,void*)>(objc_msgSend)(backend,sel_registerName("setCmdBuffer:"),buffer);
     reinterpret_cast<void(*)(void*,SEL,void*,bool)>(objc_msgSend)(backend,sel_registerName("setRenderTargetBeginDraw:setCurrentRT:"),output,true);
     puts("{\"event\":\"host_offscreen_encoder_supplied\"}");
    }
    reinterpret_cast<void(*)(void*,void*,float)>(0x1007bc41c+slide)(window,target,1.0f);
    puts("{\"event\":\"panel_draw_returned\"}");
    alignas(16) unsigned char readback[512]={};reinterpret_cast<void(*)(void*)>(0x100366bc8+slide)(readback);int stride=0;
    bool copied=reinterpret_cast<bool(*)(void*,void*,void*,void*,size_t,int*,bool)>(0x1006d4dac+slide)(target,output,readback,nullptr,0,&stride,false);
    printf("{\"event\":\"readback_result\",\"accepted\":%s,\"stride\":%d,\"width\":%d,\"height\":%d}\n",copied?"true":"false",stride,*(int*)readback,*(int*)(readback+4));
    Require(copied&&stride==320*4&&*(int*)readback==320&&*(int*)(readback+4)==200,"readback failed");
    auto pixels=Read(*(uint64_t*)(readback+0x28),320*200*4);std::ofstream raw("render.bgra",std::ios::binary);raw.write((char*)pixels.data(),pixels.size());raw.close();

   }
   if(ok&&mode=="draw") {
    puts("{\"event\":\"before_draw\"}");reinterpret_cast<void(*)(void*)>(0x1004a4490+slide)(window);puts("{\"event\":\"draw_returned\"}");
   }
  }
  puts("{\"event\":\"complete\"}");_Exit(0);
 }catch(const std::exception& e){fprintf(stderr,"skin host stopped: %s\n",e.what());_Exit(1);}
}

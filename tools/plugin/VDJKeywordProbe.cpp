// Public SDK only: fixed is_using keyword/control sweep, repeatable by a plugin button.
#include "vdjDsp8.h"
#include "is_using_cases.h"
#include <cstdio>
#include <cstdlib>
#include <string>
#include <ctime>
#include <sys/stat.h>
#include <unistd.h>
#include <cstring>
class KeywordProbe:public IVdjPluginDsp8 {
    int captureButton=0;
    bool ready=false, busy=false;
    unsigned serial=0;
    void Capture() {
        if(busy)return;busy=true;
        const char* home=getenv("HOME");if(!home){busy=false;return;}
        std::string dir=std::string(home)+"/Library/Application Support/VirtualDJ/VDJIntrospect";mkdir(dir.c_str(),0755);
        auto now=time(nullptr);
        std::string path=dir+"/keywords-"+std::to_string(getpid())+"-"+std::to_string(now)+"-"+std::to_string(++serial)+".jsonl";
        FILE* f=fopen(path.c_str(),"wx");if(!f){busy=false;return;}
        double build=0;auto bhr=cb->GetInfo("get_build",&build);
        fprintf(f,"{\"event\":\"start\",\"build\":%.0f,\"build_hresult\":%d,\"captured_unix\":%lld}\n",build,(int)bhr,(long long)now);fflush(f);
        for(int round=1;round<=2;round++)for(auto script:kKeywordCases) {
            double value=0;char text[128]={};
            auto hr=cb->GetInfo(script,&value);auto thr=cb->GetStringInfo(script,text,sizeof(text));
            // Only emit the expected boolean/empty rendering, never arbitrary text.
            bool known=!strcmp(text,"") || !strcmp(text,"off") || !strcmp(text,"on") || !strcmp(text,"no") || !strcmp(text,"yes");
            fprintf(f,"{\"event\":\"case\",\"round\":%d,\"script\":\"%s\",\"numeric_hresult\":%d,\"numeric_value\":%.17g,\"text_hresult\":%d,\"text\":\"%s\"}\n",round,script,(int)hr,value,(int)thr,known?text:"REDACTED_UNEXPECTED");fflush(f);
        }
        fputs("{\"event\":\"complete\"}\n",f);fclose(f);busy=false;
    }
    HRESULT VDJ_API OnGetPluginInfo(TVdjPluginInfo8* info) override {
        info->PluginName="VDJKeywordProbe";info->Author="virtualdj-api-reference";info->Description="Fixed public-query keyword/control capture";
        info->Version="0.1";info->Bitmap=nullptr;info->Flags=0;return S_OK;
    }
    HRESULT VDJ_API OnLoad() override {
        DeclareParameterButton(&captureButton,0,"Capture","Capture");ready=true;Capture();return S_OK;
    }
    HRESULT VDJ_API OnParameter(int id) override {if(ready && id==0 && captureButton)Capture();return S_OK;}
    HRESULT VDJ_API OnProcessSamples(float*,int) override{return S_OK;}
};
extern "C" VDJ_EXPORT HRESULT VDJ_API DllGetClassObject(const GUID& cls,const GUID& iid,void** out) {
    if(!out)return static_cast<HRESULT>(0x80004005);*out=nullptr;
    if(memcmp(&cls,&CLSID_VdjPlugin8,sizeof(cls)) || memcmp(&iid,&IID_IVdjPluginDsp8,sizeof(iid)))return CLASS_E_CLASSNOTAVAILABLE;
    *out=static_cast<IVdjPluginDsp8*>(new KeywordProbe);return S_OK;
}

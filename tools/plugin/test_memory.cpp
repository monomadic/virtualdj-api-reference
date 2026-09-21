#include "VDJMemoryProbe.cpp"
#include <cassert>
#include <functional>
static bool Fails(std::function<void()> f) { try { f(); } catch(const std::runtime_error&) { return true; } return false; }
int main() {
    const char names[]="\0action_deck\0hot_cue\0zoom_vertical\0";
    std::vector<uint8_t> strings(names,names+sizeof(names));
    std::vector<uint8_t> data(64,0);
    uint64_t base=0x100000000;
    size_t offsets[]={1,13,21};
    for(int i=0;i<3;i++) {
        uint64_t p=base+offsets[i]; uint32_t id=i;
        memcpy(data.data()+i*16,&p,8); memcpy(data.data()+i*16+8,&id,4);
    }
    auto table=Locate(data,strings,base);
    assert(table.offset==0 && table.records.size()==3 && table.records[0].id==0);
    Record r;
    assert(!Decode(data,60,strings,base,r));
    assert(!Decode(data,SIZE_MAX,strings,base,r));
    assert(!Decode(data,0,strings,base+1,r));
    auto bad=data; uint64_t p=UINT64_MAX; memcpy(bad.data()+16,&p,8);
    assert(Fails([&]{Locate(bad,strings,base);}));
    auto duplicate=data; duplicate.insert(duplicate.end(),data.begin(),data.end());
    assert(Fails([&]{Locate(duplicate,strings,base);}));
    auto unsorted=data; memcpy(unsorted.data(),data.data()+32,16);
    assert(Fails([&]{Locate(unsorted,strings,base);}));
    assert(Fails([]{Read(0,16);}));
    assert(Fails([]{Read(0,33*1024*1024);}));
    uint64_t known=0x0123456789abcdef;
    auto copied=Read(reinterpret_cast<uint64_t>(&known),sizeof(known));
    assert(!memcmp(copied.data(),&known,sizeof(known)));
    assert(Fails([]{Capture(nullptr);})); // A fake host must never produce a live capture.
    puts("memory probe checks passed");
}

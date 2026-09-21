#include "VDJParserProbe.cpp"
#include <cassert>
int main() {
    bool rejected=false;try{GuardHost();}catch(const std::runtime_error&){rejected=true;}
    assert(rejected); // Never invoke private code outside the exact host.
    std::vector<uint8_t> p(40,0); memcpy(p.data()+8,"cue",3);p[31]=3;
    assert(ParameterText(p,"is_using cue")=="cue");
    rejected=false;try{ParameterText(p,"is_using zzunknowna");}catch(const std::runtime_error&){rejected=true;}assert(rejected);
    p[31]=23;rejected=false;try{ParameterText(p,"is_using cue");}catch(const std::runtime_error&){rejected=true;}assert(rejected);
    rejected=false;try{Field<uint64_t>(p,39);}catch(const std::runtime_error&){rejected=true;}assert(rejected);
    puts("parser probe guards and bounded string checks passed");
}

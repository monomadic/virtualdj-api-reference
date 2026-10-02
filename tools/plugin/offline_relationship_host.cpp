// Reuse the bounded composition reader; arm debugger probes only after code hashes pass.
#include <cstdio>
#include <cstring>
__attribute__((noinline)) void RelationshipTraceReady() { asm volatile(""); }
int RelationshipPuts(const char* text) {
    int result = puts(text);
    if (strcmp(text, "{\"event\":\"composition_guards_passed\"}") == 0)
        RelationshipTraceReady();
    return result;
}
#define puts RelationshipPuts
#include "offline_composition_host.cpp"
#undef puts

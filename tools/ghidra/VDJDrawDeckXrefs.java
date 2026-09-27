import java.io.FileWriter;
import java.util.*;

import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.symbol.SymbolTable;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceManager;

public class VDJDrawDeckXrefs extends GhidraScript {

    String[] targets = new String[] {
        "__ZN7CPlugin8DrawDeckEv",
        "__ZThn8_N7CPlugin8DrawDeckEv",
        "__ZN12CVideoEngine8DrawDeckEi",
        "__ZN12CVideoEngine9_DrawDeckEiP7TVertex"
    };

    @Override
    public void run() throws Exception {
        FunctionManager fm = currentProgram.getFunctionManager();
        SymbolTable symtab = currentProgram.getSymbolTable();
        ReferenceManager refmgr = currentProgram.getReferenceManager();

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);

        StringBuilder out = new StringBuilder();

        for (String tname : targets) {
            List<Symbol> syms = new ArrayList<>();
            for (Symbol s : symtab.getSymbols(tname)) syms.add(s);
            if (syms.isEmpty()) {
                out.append("=== target ").append(tname).append(" NOT FOUND ===\n");
                continue;
            }
            for (Symbol sym : syms) {
                Address addr = sym.getAddress();
                Function func = fm.getFunctionAt(addr);
                out.append("=== target ").append(tname).append(" @ ").append(addr)
                   .append(" func=").append(func != null ? func.getName() : "null").append(" ===\n");

                Set<Function> callers = new LinkedHashSet<>();
                for (Reference ref : refmgr.getReferencesTo(addr)) {
                    Address from = ref.getFromAddress();
                    Function callerFunc = fm.getFunctionContaining(from);
                    if (callerFunc != null) {
                        callers.add(callerFunc);
                    } else {
                        out.append("  raw ref from ").append(from).append(" (no containing function)\n");
                    }
                }
                if (callers.isEmpty()) {
                    out.append("  (no references found)\n");
                }
                for (Function cf : callers) {
                    out.append("  caller: ").append(cf.getName())
                       .append(" @ ").append(cf.getEntryPoint()).append("\n");
                }
            }
        }

        // Decompile CPlugin::DrawDeck() body itself
        for (Symbol sym : symtab.getSymbols("__ZN7CPlugin8DrawDeckEv")) {
            Function func = fm.getFunctionAt(sym.getAddress());
            if (func != null) {
                DecompileResults res = decomp.decompileFunction(func, 60, monitor);
                out.append("=== decompiled body: CPlugin::DrawDeck ===\n");
                if (res.decompileCompleted()) {
                    out.append(res.getDecompiledFunction().getC()).append("\n");
                } else {
                    out.append("  decompile failed: ").append(res.getErrorMessage()).append("\n");
                }
            }
        }

        // Decompile every caller of CPlugin::DrawDeck()
        for (Symbol sym : symtab.getSymbols("__ZN7CPlugin8DrawDeckEv")) {
            Set<Address> seen = new LinkedHashSet<>();
            for (Reference ref : refmgr.getReferencesTo(sym.getAddress())) {
                Function callerFunc = fm.getFunctionContaining(ref.getFromAddress());
                if (callerFunc != null && seen.add(callerFunc.getEntryPoint())) {
                    DecompileResults res = decomp.decompileFunction(callerFunc, 60, monitor);
                    out.append("=== decompiled caller: ").append(callerFunc.getName()).append(" ===\n");
                    if (res.decompileCompleted()) {
                        out.append(res.getDecompiledFunction().getC()).append("\n");
                    } else {
                        out.append("  decompile failed: ").append(res.getErrorMessage()).append("\n");
                    }
                }
            }
        }

        // Also trace callers of CVideoEngine::DrawDeck(int) and decompile them (shallow, names only + one decompile each)
        for (String tname : new String[]{"__ZN12CVideoEngine8DrawDeckEi", "__ZN12CVideoEngine9_DrawDeckEiP7TVertex"}) {
            for (Symbol sym : symtab.getSymbols(tname)) {
                Set<Address> seen = new LinkedHashSet<>();
                for (Reference ref : refmgr.getReferencesTo(sym.getAddress())) {
                    Function callerFunc = fm.getFunctionContaining(ref.getFromAddress());
                    if (callerFunc != null && seen.add(callerFunc.getEntryPoint())) {
                        out.append("caller-of-").append(tname).append(": ")
                           .append(callerFunc.getName()).append(" @ ").append(callerFunc.getEntryPoint()).append("\n");
                    }
                }
            }
        }

        FileWriter fw = new FileWriter("/private/tmp/claude-501/-Users-nom-src-virtualdj-plugin-upnext/338b0504-5d14-4452-9bdd-99ba251642d0/scratchpad/drawdeck_callers.txt");
        fw.write(out.toString());
        fw.close();
        println("DONE wrote " + out.length() + " chars");
    }
}

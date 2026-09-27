import java.io.FileWriter;
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionManager;
import ghidra.program.model.address.Address;

public class VDJDecompileThree extends GhidraScript {
    @Override
    public void run() throws Exception {
        FunctionManager fm = currentProgram.getFunctionManager();
        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);
        StringBuilder out = new StringBuilder();
        String[] addrs = new String[]{"1007f5fcc", "1002a0b90", "1007425b4"};
        for (String a : addrs) {
            Address addr = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(Long.parseLong(a, 16));
            Function f = fm.getFunctionAt(addr);
            out.append("=== ").append(f != null ? f.getName(true) : "null").append(" @ ").append(a).append(" ===\n");
            if (f != null) {
                DecompileResults res = decomp.decompileFunction(f, 90, monitor);
                if (res.decompileCompleted()) {
                    out.append(res.getDecompiledFunction().getC()).append("\n");
                } else {
                    out.append("decompile failed: ").append(res.getErrorMessage()).append("\n");
                }
            }
        }
        FileWriter fw = new FileWriter("/private/tmp/claude-501/-Users-nom-src-virtualdj-plugin-upnext/338b0504-5d14-4452-9bdd-99ba251642d0/scratchpad/three_callers.txt");
        fw.write(out.toString());
        fw.close();
        println("DONE " + out.length());
    }
}

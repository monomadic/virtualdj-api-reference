// Export bounded decompilation from an already analyzed project, without mutation.
// @category VirtualDJ
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.framework.Application;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import com.google.gson.GsonBuilder;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

public class VDJTailExport extends GhidraScript {
    private String sha(byte[] bytes) throws Exception {
        StringBuilder text = new StringBuilder();
        for (byte b : MessageDigest.getInstance("SHA-256").digest(bytes))
            text.append(String.format("%02x", b & 255));
        return text.toString();
    }
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 3 || args.length % 2 != 1)
            throw new IllegalArgumentException("output followed by address/length pairs required");
        Map<String,Object> result = new LinkedHashMap<>();
        result.put("ghidra_version", Application.getApplicationVersion());
        result.put("program_name", currentProgram.getName());
        result.put("program_sha256", currentProgram.getExecutableSHA256());
        result.put("language", currentProgram.getLanguageID().toString());
        result.put("compiler_spec", currentProgram.getCompilerSpec().getCompilerSpecID().toString());
        result.put("evidence_tier", 2);
        ArrayList<Object> rows = new ArrayList<>();
        DecompInterface decompiler = new DecompInterface();
        try {
            if (!decompiler.openProgram(currentProgram)) throw new IllegalStateException(decompiler.getLastMessage());
            for (int i=1; i<args.length; i+=2) {
                Address address = toAddr(args[i]);
                int length = Integer.parseInt(args[i+1]);
                if (length <= 0 || length > 16384) throw new IllegalArgumentException("invalid bounds");
                Function function = currentProgram.getFunctionManager().getFunctionAt(address);
                if (function == null) throw new IllegalStateException("no function at " + address);
                byte[] bytes = new byte[length];
                if (currentProgram.getMemory().getBytes(address, bytes) != length) throw new IllegalStateException("short read");
                DecompileResults d = decompiler.decompileFunction(function, 60, monitor);
                if (!d.decompileCompleted()) throw new IllegalStateException(d.getErrorMessage());
                Map<String,Object> row = new LinkedHashMap<>();
                row.put("address", "0x" + address);
                row.put("guard_length", length);
                row.put("guard_sha256", sha(bytes));
                row.put("ghidra_name", function.getName(true));
                row.put("body_min", function.getBody().getMinAddress().toString());
                row.put("body_max", function.getBody().getMaxAddress().toString());
                row.put("warning", d.getErrorMessage());
                row.put("decompiled_c", d.getDecompiledFunction().getC());
                rows.add(row);
            }
        } finally { decompiler.dispose(); }
        result.put("functions", rows);
        result.put("scope", "Decompiler interpretation of an existing project; no auto-analysis or program mutation. Guard bytes must match independently extracted binary intervals. Not runtime evidence.");
        Files.writeString(Path.of(args[0]), new GsonBuilder().setPrettyPrinting().create().toJson(result) + "\n", StandardOpenOption.CREATE_NEW);
        println("Exported " + rows.size() + " bounded functions");
    }
}

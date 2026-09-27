import java.io.FileWriter;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.symbol.SymbolTable;
import ghidra.program.model.symbol.SymbolIterator;

public class VDJFindSymbols extends GhidraScript {
    @Override
    public void run() throws Exception {
        SymbolTable symtab = currentProgram.getSymbolTable();
        StringBuilder out = new StringBuilder();
        SymbolIterator it = symtab.getSymbolIterator();
        int count = 0;
        while (it.hasNext()) {
            Symbol s = it.next();
            String n = s.getName();
            if (n.contains("DrawDeck")) {
                out.append(s.getAddress()).append("  ").append(n)
                   .append("  type=").append(s.getSymbolType())
                   .append("  source=").append(s.getSource())
                   .append("\n");
                count++;
            }
        }
        out.append("TOTAL=").append(count).append("\n");
        FileWriter fw = new FileWriter("/private/tmp/claude-501/-Users-nom-src-virtualdj-plugin-upnext/338b0504-5d14-4452-9bdd-99ba251642d0/scratchpad/symbol_search.txt");
        fw.write(out.toString());
        fw.close();
        println("DONE " + count);
    }
}

import com.cburch.logisim.file.*;
import com.cburch.logisim.proj.Project;
import com.cburch.logisim.circuit.*;
import com.cburch.logisim.instance.*;
import com.cburch.logisim.std.wiring.Pin;
import com.cburch.logisim.data.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
/** Drive the real Logisim circuit engine with stateful vectors; never evaluate gates here. */
public class CircuitRunner {
  public static void main(String[] args) throws Exception {
    try { perform(args); } catch(Throwable error) { error.printStackTrace();System.exit(2); }
  }
  private static void perform(String[] args) throws Exception {
    com.cburch.logisim.Main.headless=true;
    if(args.length<3 || args.length%2!=1)throw new IllegalArgumentException("circ circuit vectors [circuit vectors]...");
    com.cburch.logisim.file.LogisimFile loaded;
    try(var raw=new FileInputStream(args[0])){loaded=new StrictLoader().openLogisimFile(raw);}
    var project=new Project(loaded);int total=0,failures=0;
    for(int job=1;job<args.length;job+=2){
      var circuit=loaded.getCircuit(args[job]);
      if(circuit==null)throw new IllegalArgumentException("Missing circuit "+args[job]);
      var pins=new LinkedHashMap<String,Instance>();
      for(var e:Analyze.getPinLabels(circuit).entrySet())pins.put(e.getValue(),e.getKey());
      var labeled=new HashMap<String,Instance>();
      for(var component:circuit.getNonWires())if(component.getAttributeSet().containsAttribute(StdAttr.LABEL)){
        var label=component.getAttributeSet().getValue(StdAttr.LABEL);
        if(label!=null&&!label.isEmpty())labeled.put(label,Instance.getInstanceFor(component));
      }
      var lines=Files.readAllLines(Path.of(args[job+1]));String[] header=null;int count=0,failed=0;
      var state=CircuitState.createRootState(project,circuit);
      for(String line:lines){
        line=line.trim();if(line.isEmpty()||line.startsWith("#"))continue;
        if(line.equals("!reset")){state=CircuitState.createRootState(project,circuit);continue;}
        if(header==null){header=line.split("\\s+");for(String h:header)if(!h.equals("OSC")&&!pins.containsKey(h)&&!(h.contains("@")&&labeled.containsKey(h.split("@")[0])))throw new IllegalArgumentException("Unknown pin/component "+h+" in "+pins.keySet());continue;}
        var values=line.split("\\s+");if(values.length!=header.length)throw new IllegalArgumentException("Vector width mismatch: "+line);
        for(int i=0;i<header.length;i++){
          var pin=pins.get(header[i]);if(pin==null||!Pin.FACTORY.isInputPin(pin))continue;
          if(values[i].equals("-"))continue;
          var width=pin.getAttributeValue(StdAttr.WIDTH);
          var s=values[i];long n=s.startsWith("0x")?Long.parseUnsignedLong(s.substring(2),16):Long.parseLong(s);
          var pinState=state.getInstanceState(pin);
          Pin.FACTORY.driveInputPin(pinState,Value.createKnown(width,n));
          pinState.fireInvalidated();
        }
        state.getPropagator().propagate();boolean ok=true;var actual=new ArrayList<String>();
        for(int i=0;i<header.length;i++){
          if(header[i].equals("OSC")){boolean osc=state.getPropagator().isOscillating();actual.add("OSC="+(osc?1:0));if(!values[i].equals("-")&&osc!=values[i].equals("1"))ok=false;continue;}
          Value v;
          if(header[i].contains("@")){
            var parts=header[i].split("@");v=state.getInstanceState(labeled.get(parts[0])).getPortValue(Integer.parseInt(parts[1]));
          }else{
            var pin=pins.get(header[i]);if(Pin.FACTORY.isInputPin(pin))continue;
            v=Pin.FACTORY.getValue(state.getInstanceState(pin));
          }
          actual.add(header[i]+"="+v.toBinaryString());
          if(values[i].equals("-"))continue;
          if(values[i].equals("X")){if(v.isFullyDefined())ok=false;continue;}
          long n=values[i].startsWith("0x")?Long.parseUnsignedLong(values[i].substring(2),16):Long.parseLong(values[i]);
          if(!v.isFullyDefined()||v.toLongValue()!=n)ok=false;
        }
        if(!ok){failed++;if(failed<=12)System.out.println("MISMATCH "+args[job]+" row="+count+" vector="+line+" actual="+String.join(",",actual));}
        if(System.getProperty("trace","false").equals("true"))System.out.println("TRACE "+args[job]+" "+count+" "+String.join(",",actual));
        count++;
      }
      total+=count;failures+=failed;System.out.println("RESULT "+args[job]+" vectors="+count+" failures="+failed);
    }
    System.out.println("TOTAL vectors="+total+" failures="+failures);System.exit(failures==0?0:1);
  }
}

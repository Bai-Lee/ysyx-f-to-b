import com.cburch.logisim.file.*;
import com.cburch.logisim.proj.Project;
import com.cburch.logisim.circuit.*;
import com.cburch.logisim.data.*;
import java.io.*;
public class CircuitInspect {
  public static void main(String[] args)throws Exception{
    try{perform(args);}catch(Throwable error){error.printStackTrace();System.exit(2);}
  }
  private static void perform(String[] args)throws Exception{
    com.cburch.logisim.Main.headless=true;
    com.cburch.logisim.file.LogisimFile f;
    try(var raw=new FileInputStream(args[0])){f=new StrictLoader().openLogisimFile(raw);}
    var c=f.getCircuit(args[1]);
    if(args.length>2)for(var library:f.getLibraries()){System.out.print("LIB "+library.getName()+": ");for(var tool:library.getTools())System.out.print(tool.getName()+", ");System.out.println();}
    for(var comp:c.getNonWires()){
      System.out.println(comp.getFactory().getName()+" "+comp.getLocation()+" ends="+comp.getEnds());
      for(var end:comp.getEnds())System.out.println("    PORT "+end.getLocation()+" width="+end.getWidth()+" input="+end.isInput()+" output="+end.isOutput());
      var a=comp.getAttributeSet();for(Attribute k:a.getAttributes())System.out.println("  "+k.getName()+"="+a.getValue(k));
    }
    System.exit(0);
  }
}

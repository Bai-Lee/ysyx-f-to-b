import java.util.*;
import java.util.prefs.*;
/** Process-local preferences: no Windows registry or user profile modifications. */
public final class LocalPrefsFactory implements PreferencesFactory {
  private final Preferences user=new Memory(null,"");
  private final Preferences system=new Memory(null,"");
  public Preferences userRoot(){return user;}
  public Preferences systemRoot(){return system;}
  private static final class Memory extends AbstractPreferences {
    private final Map<String,String> values=new HashMap<>();
    private final Map<String,Memory> children=new HashMap<>();
    Memory(AbstractPreferences parent,String name){super(parent,name);}
    protected void putSpi(String k,String v){values.put(k,v);}
    protected String getSpi(String k){return values.get(k);}
    protected void removeSpi(String k){values.remove(k);}
    protected void removeNodeSpi(){values.clear();children.clear();}
    protected String[] keysSpi(){return values.keySet().toArray(new String[0]);}
    protected String[] childrenNamesSpi(){return children.keySet().toArray(new String[0]);}
    protected AbstractPreferences childSpi(String n){return children.computeIfAbsent(n,x->new Memory(this,x));}
    protected void syncSpi(){}
    protected void flushSpi(){}
  }
}

/** Parse warnings/errors are fatal; never silently drop an unrecognized component. */
public class StrictLoader extends com.cburch.logisim.file.Loader {
  public StrictLoader(){super(null);}
  @Override public void showError(String message){throw new IllegalArgumentException("Logisim load: "+message);}
}

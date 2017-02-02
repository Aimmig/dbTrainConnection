package dbapi;

import java.util.ArrayList;
import java.util.HashMap;
import javax.swing.SwingUtilities;
/**

 * @author Andre Immig
 * aimmig@students.uni-mainz.de
 */
public class DBApi {

    //global variables
    //bahnhofID stores intern representation of <Name,Id>
    public static ArrayList<String> stations=new ArrayList<>();
    public static HashMap<String,String> stationID=new HashMap<>();
    
    public static DBGuiAPI frame;
    
    //key
    public static final String KEY="DBhackFrankfurt0316";
    //language
    public static final String LAN="de";

    //saves the history of searching connections
    public static ArrayList<ConnectionList> history=new ArrayList<>();
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> 
            frame=new DBGuiAPI());
    };
}            

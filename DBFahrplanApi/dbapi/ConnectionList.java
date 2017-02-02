package dbapi;

import java.io.Serializable;

/**
 *
 * @author Andre Immig
 *  aimmig@students.uni-mainz.de
 */
public class ConnectionList implements Serializable {
    private Connection [] conArray;
    private int maxNameLength;
    private int maxStopLength;
    private String labelText;

    //default constructor
    public ConnectionList(){}
    
    public String getLabelText() {
        return labelText;
    }

    public void setLabelText(String labelText) {
        this.labelText = labelText;
    }

    public Connection[] getConArray() {
        return conArray;
    }

    public void setConArray(Connection[] conArray) {
        this.conArray = conArray;
    }
    
    public void createConArray(int length){
        this.conArray=new Connection [length];
    }

    public int getMaxNameLength() {
        return maxNameLength;
    }

    public void setMaxNameLength(int maxNameLength) {
        this.maxNameLength = maxNameLength;
    }
    
    public void setConnectionAtIndex(Connection c,int i){
        conArray[i]=c;
    }
    
    public Connection getConnectionAtIndex(int i){
        return conArray[i];
    }
    
    public int getMaxStopLength() {
        return maxStopLength;
    }

    public void setMaxStopLength(int maxStopLength) {
        this.maxStopLength = maxStopLength;
    }
    
}

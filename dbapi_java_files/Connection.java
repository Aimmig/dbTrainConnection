package dbapi;

import java.io.Serializable;
import java.net.MalformedURLException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;


/**
 *
 * @author Andre Immig
 *  aimmig@students.uni-mainz.de
 */
public class Connection implements Serializable {
    private Date date;
    private String direction;
    private String name;
    private String stop;
    private String stopID;
    private String time;
    //may be null if no train type availabel
    private String type;
    //may be null if no track available
    private String track;
    private String details;
    private ArrayList<Stop> stopList;
    private int maxStopNameLength;
    private boolean isDeparture;
    private static final SimpleDateFormat outputFormat=new SimpleDateFormat("dd.MM.yyyy");
    private byte[] image;
    
    public Connection(){}

    public Connection(String dateString, String direction, String name, String stop, String stopID, String time, String type, String track, String url,Boolean dep) throws MalformedURLException {
        //map=null;
        date=null;
        try{
            String [] splitted=dateString.split("-");
            StringBuilder formatted=new StringBuilder(splitted[2]);
            formatted.append(".").append(splitted[1]).append(".").append(splitted[0]);
            this.date=outputFormat.parse(formatted.toString());
        } catch (ParseException|java.lang.IndexOutOfBoundsException ex) {}
        this.direction = direction;
        this.name = name;
        this.stop = stop;
        this.stopID = stopID;
        this.time = time;
        this.type = type;
        this.details =url;
        this.track=track;
        this.stopList=null;
        this.maxStopNameLength=0;
        this.isDeparture=dep;
       
    }
    
    //tries to add a stop to list
    public void addStopToList(Stop s){
        //add stop to list
        if(stopList!=null){
            stopList.add(s);
        }
        //add first entry to stop list
        else{
            stopList=new ArrayList<>();
            stopList.add(s);
        }
    }
    
    public byte[] getImage(){
        return image;
    }

    public String getDirection() {
        return direction;
    }

    public String getName() {
        return name;
    }

    public String getStop() {
        return stop;
    }

    public String getStopID() {
        return stopID;
    }

    public String getTime() {
        return time;
    }

    public String getType() {
        return type;
    }

    public String getTrack() {
        return track;
    }

    public String getDetails() {
        return details;
    }
    
    public String getDate() {
        return outputFormat.format(date);
    }

    public ArrayList<Stop> getStopList() {
        return stopList;
    }

    public int getMaxStopNameLength() {
        return maxStopNameLength;
    }

    public boolean isIsDeparture() {
        return isDeparture;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public void setDirection(String direction) {
        this.direction = direction;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setStop(String stop) {
        this.stop = stop;
    }

    public void setStopID(String stopID) {
        this.stopID = stopID;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public void setType(String type) {
        this.type = type;
    }

    public void setTrack(String track) {
        this.track = track;
    }

    public void setDetails(String details) {
        this.details = details;
    }
    
    public void setImage(byte [] bytearray){
       this.image=bytearray;
    }

    public void setStopList(ArrayList<Stop> stopList) {
        this.stopList = stopList;
    }

    public void setMaxStopNameLength(int maxStopNameLength) {
        this.maxStopNameLength = maxStopNameLength;
    }

    public void setIsDeparture(boolean isDeparture) {
        this.isDeparture = isDeparture;
    }
    
    //returns nicely formated StringRepresentation for ComboBox
    //fills name and direction with "" if shorter than requested
    public String toString(int nameLength,int directionLength){
        StringBuilder result=new StringBuilder(name);
        while(result.length()<=nameLength){
            result.append(" ");
        }
        if(isDeparture){
            result.append("  nach ");
        }
        else{
            result.append("  von ");
        }
        int l=result.length();
        result.append(direction);
        while(result.length()<l+directionLength){
            result.append(" ");
        }
        result.append(" ").append(" ");
        result.append(" um ").append(time);
        if(track!=null){
            if(isDeparture){
                result.append("    Gleis ");
            }
            else{
                result.append("    Gleis ");
            }
            result.append(track);
        }
        return result.toString();
    }
    
    @Override
    //returns name von start nach destination
    public String toString(){
        StringBuilder result=new StringBuilder(" Zugverlauf ");
        result.append(name);
        Stop start=stopList.get(0);
        Stop destination=stopList.get(stopList.size()-1);
        result.append(" von ").append(start.getName());
        result.append(" nach ").append(destination.getName());
        String dep=start.getDeparture().split(" ")[0];
        String [] splitted=dep.split("-");
        StringBuilder formatted=new StringBuilder(splitted[2]);
        formatted.append(".").append(splitted[1]).append(".").append(splitted[0]);
        result.append(" am ").append(formatted.toString());
        return result.toString();
    }
}

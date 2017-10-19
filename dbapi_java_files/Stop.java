
package dbapi;

import java.io.Serializable;

/**
 *
 * @author Andre Immig
 *  aimmig@students.uni-mainz.de
 */
public class Stop implements Serializable {
    private String name;
    private String id;
    private String arrTime;
    private String arrDate;
    private String depTime;
    private String depDate;
    private String track;
    private double longitude;
    private double latitude;
    
    public Stop(){}
    
    public Stop(String name, String id, String arrTime, String arrDate, String depTime, String depDate, String track, double lon,double lat) {
        this.name = name;
        this.id = id;
        this.arrTime = arrTime;
        this.arrDate = arrDate;
        this.depTime = depTime;
        this.depDate = depDate;
        this.track = track;
        this.longitude=lon;
        this.latitude=lat;
    }
    
    public double getLongitude() {
        return longitude;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setId(String id) {
        this.id = id;
    }

    public void setTrack(String track) {
        this.track = track;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public String getArrTime() {
        return arrTime;
    }

    public void setArrTime(String arrTime) {
        this.arrTime = arrTime;
    }

    public String getArrDate() {
        return arrDate;
    }

    public void setArrDate(String arrDate) {
        this.arrDate = arrDate;
    }

    public String getDepTime() {
        return depTime;
    }

    public void setDepTime(String depTime) {
        this.depTime = depTime;
    }

    public String getDepDate() {
        return depDate;
    }

    public void setDepDate(String depDate) {
        this.depDate = depDate;
    }

    public String getName() {
        return name;
    }

    public String getId() {
        return id;
    }

    public String getArrival() {
        if(arrDate!=null){
            return new StringBuilder(arrDate).append(" ").append(arrTime).toString();
        }
        else{
            return null;
        }
    }

    public String getDeparture() {
        if(depDate!=null){
            return new StringBuilder(depDate).append(" ").append(depTime).toString();
        }
        else{
            return null;
            
        }
    }

    public String getTrack() {
        return track;
    }
    
    public String toString(int length){
        StringBuilder result=new StringBuilder(name);
        while(result.length()<length+1){
            result.append(" ");
        }
        if(arrDate!=null){
            result.append(" Ankunft ").append(arrTime);
        }
        else{
            // " Ankunft "+hh:mm has 14 chars
            int arrLength=14;
            for(int i=0;i<arrLength;i++){
                result.append(" ");
            }
        }
        result.append("   ");
        if(depDate!=null){
            result.append(" Abfahrt ").append(depTime);
        }
        else{
            // " Abfahrt "+hh:mm has 14 chars
            int depLength=14;
            for(int i=0;i<depLength;i++){
                result.append(" ");
            }
        }
        result.append(" ").append(" ").append(" ");
        if(track!=null){
            result.append("  Gleis ").append(track);
        }
        return result.toString();
    }
    
}

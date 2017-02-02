package dbapi;

import com.sun.org.apache.xerces.internal.impl.dv.util.Base64;
import static dbapi.DBApi.KEY;
import static dbapi.DBApi.history;
import static dbapi.DBApi.stationID;
import static dbapi.DBApi.stations;
import java.awt.Dimension;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.text.ParseException;
import java.util.Calendar;
import java.util.Date;
import javax.imageio.ImageIO;
import javax.swing.JOptionPane;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

/**
 *
 * @author andre
 */
//class that handles network-connection, extracting data from wesite using xml ,writes data to public variables

public class InformationControll {
        
    //takes a date String yyyy-MM-dd and format its to dd.MM.yyyy
    public static String formatDateForOutput(String date){
        String [] splitted=date.replace(" ","-").split("-");
        StringBuilder formatted=new StringBuilder(splitted[2]);
        formatted.append(".").append(splitted[1]).append(".").append(splitted[0]).append(" ").append(splitted[3]);
        return formatted.toString();
    }
    
    //takes a formatted Date, adds given hours to date and returns formatted date
    public static String addHoursToCalendar(String formatted,int hours) throws ParseException{
        Date date=DBGuiAPI.dateFormat.parse(formatted);
        Calendar c=Calendar.getInstance();
        c.setTime(date);
        c.add(Calendar.HOUR,hours);
        return DBGuiAPI.dateFormat.format(c.getTime());
    }
    
    //gets the indexed formatted Date from Dep/Arrival table
    public static String getFormattedDate(int index){
        int beginOfDate=history.get(index).getLabelText().lastIndexOf("m")+2;
        String replaced=history.get(index).getLabelText().substring(beginOfDate).replace(".", "-").replace(" ", "-");
        String [] splitted=replaced.split("-");
        StringBuilder formatted=new StringBuilder(splitted[2]);
        formatted.append("-").append(splitted[1]).append("-").append(splitted[0]);
        formatted.append(" ").append(splitted[3]);
        return formatted.toString();
    }
    
    
    //writes stop from detail url to according connection object specifed by index
    public static void addStopsToList(Dimension d,int showIndex,int connectionIndex,String URLString) throws ParserConfigurationException, SAXException, IOException{
        StringBuilder imageUrl = new StringBuilder("http://maps.google.com/maps/api/staticmap?&size=");
        imageUrl.append((int)d.getWidth()).append("x").append((int)d.getHeight());
        imageUrl.append("&language=").append(DBApi.LAN);
        imageUrl.append("&sensor=false");
        imageUrl.append("&path=color:0xff0000ff|weight:2");
        
        StringBuilder markers=new StringBuilder("&markers=size:tiny|color:red");
        
        Document doc=getDocument(URLString);
        NodeList list=doc.getElementsByTagName("Stop");
        String name,id,arrTime,arrDate,depTime,depDate,track;
        double longitude,latitude;
        Stop act;
        //iterate over all stops of connection
        for(int i=0;i<list.getLength();i++){
           
            try{
                //arrive Date
                arrDate=list.item(i).getAttributes().getNamedItem("arrDate").getNodeValue();
                //arriveTime
                arrTime=list.item(i).getAttributes().getNamedItem("arrTime").getNodeValue();
            }
            catch(java.lang.NullPointerException e){
                arrDate=null;
                arrTime=null;
            }
            try{
                //depDate
                depDate=list.item(i).getAttributes().getNamedItem("depDate").getNodeValue();
                //depTime
                depTime=list.item(i).getAttributes().getNamedItem("depTime").getNodeValue();
            }
            catch(java.lang.NullPointerException ex){
                depDate=null;
                depTime=null;                
            }
            //stopID
            id=list.item(i).getAttributes().getNamedItem("id").getNodeValue();
            //stopName
            name=list.item(i).getAttributes().getNamedItem("name").getNodeValue();
            //long
            longitude=Double.valueOf(list.item(i).getAttributes().getNamedItem("lon").getNodeValue());
            //lat
            latitude=Double.valueOf(list.item(i).getAttributes().getNamedItem("lat").getNodeValue());
            
            imageUrl.append("|").append(latitude).append(",").append(longitude);
            markers.append("|").append(latitude).append(",").append(longitude);
            //track
            try{
                track=list.item(i).getAttributes().getNamedItem("track").getNodeValue();
            }
            catch(java.lang.NullPointerException exc){
                track=null;
            }
            act=new Stop(name,id,arrTime,arrDate,depTime,depDate,track,longitude,latitude);
            
            history.get(showIndex).getConnectionAtIndex(connectionIndex).addStopToList(act);
            //change maxStopName length
            if(name.length()>history.get(showIndex).getConnectionAtIndex(connectionIndex).getMaxStopNameLength()){
                history.get(showIndex).getConnectionAtIndex(connectionIndex).setMaxStopNameLength(name.length());
            }    
        }
        imageUrl.append(markers.toString());
        URL mapUrl = new URL(imageUrl.toString());
        byte [] bytearray=null;
        BufferedImage image=ImageIO.read(mapUrl);
        String base64String;
        try (ByteArrayOutputStream baos = new ByteArrayOutputStream(1000)) {
            ImageIO.write(image,"jpg",baos);
            baos.flush();
            base64String = Base64.encode(baos.toByteArray());
        }
        bytearray=Base64.decode(base64String);
        
        //save byteArray version of image
        history.get(showIndex).getConnectionAtIndex(connectionIndex).setImage(bytearray);
    }    
    
    //reads information from Document and writes them 
    public static boolean getInformation(String [] input,boolean departure) throws IOException{
        try{
            Document doc = getDocument(input,departure);
            
            NodeList list;
            
            //requesting stations
            switch(input.length){
                case 2:{
                    //creat List of all StopLocations
                    list=doc.getElementsByTagName("StopLocation");
                    String name;
                    String id;
                
                    //iterate over list of stop locations and get information
                    for(int i=0;i<list.getLength();i++){
                        name=list.item(i).getAttributes().getNamedItem("name").getNodeValue();
                        id=list.item(i).getAttributes().getNamedItem("id").getNodeValue();
                        stationID.put(name,id);
                        stations.add(name);
                    }
                    return true;
                }
            
                //requesting departures or arrivals
                case 3:{
                    
                    int length=history.size();
                    if(departure){
                        list=doc.getElementsByTagName("Departure");
                    }
                    else{
                        list=doc.getElementsByTagName("Arrival");
                    }
                    
                    if(list.getLength()>0){
                        history.add(new ConnectionList());                        
                
                        NodeList details=doc.getElementsByTagName("JourneyDetailRef");
                
                        String date,direction=null,time,name,stop,stopID,type,track,detailURL;
                        //iterate over all connections
                        for(int i=0;i<list.getLength();i++){
                            //Datum
                            date=list.item(i).getAttributes().getNamedItem("date").getNodeValue();
                        
                            //name
                            name=list.item(i).getAttributes().getNamedItem("name").getNodeValue();
                            //abfahrtsbahnhof Name
                            stop=list.item(i).getAttributes().getNamedItem("stop").getNodeValue();
                            //abfahrtsbahnhof id
                            stopID=list.item(i).getAttributes().getNamedItem("stopid").getNodeValue();
                            //abfahrtszeit
                            time=list.item(i).getAttributes().getNamedItem("time").getNodeValue();
                            //detail-url
                            detailURL=details.item(i).getAttributes().getNamedItem("ref").getNodeValue();
                            //Zug-Typ
                            try{
                                type=list.item(i).getAttributes().getNamedItem("type").getNodeValue();
                            }
                            //no train type available 
                            catch(java.lang.NullPointerException excep){
                                type=null;
                            }
                            if(departure){
                                direction=list.item(i).getAttributes().getNamedItem("direction").getNodeValue();
                            }
                            else{
                                direction=list.item(i).getAttributes().getNamedItem("origin").getNodeValue();
                            }    
                            if(direction.length()>history.get(length).getMaxStopLength()){
                                history.get(length).setMaxStopLength(direction.length());
                            }
                            if(name.length()>history.get(length).getMaxNameLength()){
                                history.get(length).setMaxNameLength(name.length());
                            }
                            try{
                                //if connection has track information
                                track=list.item(i).getAttributes().getNamedItem("track").getNodeValue();
                            }
                            //no track information
                            catch(java.lang.NullPointerException e){
                                track=null;
                            }   
                            Connection c=new Connection(date,direction,name,stop,stopID,time,type,track,detailURL,departure);
                            if(history.get(length).getConArray()==null){
                                history.get(length).createConArray(list.getLength());
                            }          
                            history.get(length).getConArray()[i]=c;
                            direction=null;
                        }
                        return true;
                    }
                    else{
                        return false;
                    }
                }
            }
        }    
        catch (ParserConfigurationException | SAXException ex) {
           JOptionPane.showMessageDialog(DBApi.frame,"Ursprung: "+ex.getClass()+": "+ex.getMessage(),"Fehler",JOptionPane.ERROR_MESSAGE);
           ex.printStackTrace(System.out);
           return false;
        }
        return false;
    }    
             
    //returns xml-Document from input stream
    private static Document getDocument(String [] input,boolean departure) throws ParserConfigurationException, MalformedURLException, SAXException, IOException{
        
        //xml-Document stuff
        DocumentBuilderFactory dbFactory=DocumentBuilderFactory.newInstance();
        DocumentBuilder dBuilder=dbFactory.newDocumentBuilder();
        //create xml doc from url input stream
        Document doc=dBuilder.parse(getStream(input,departure));
        doc.getDocumentElement().normalize();
        return doc;
    }
    
    private static Document getDocument(String URLString) throws ParserConfigurationException, SAXException, IOException{
        
        //xml-Document stuff
        DocumentBuilderFactory dbFactory=DocumentBuilderFactory.newInstance();
        DocumentBuilder dBuilder=dbFactory.newDocumentBuilder();
        //create xml doc from url input stream
        Document doc=dBuilder.parse(streamFromURL(URLString));
        doc.getDocumentElement().normalize();
        return doc;
    }

    //get the inputStream containing the website with user input
    private static InputStream getStream(String [] input,boolean departure) throws UnsupportedEncodingException, MalformedURLException, IOException{
        
        //Encoding URL-Format
        String enc="UTF-8";  
        
        for (int i=0;i<input.length;i++){
            input[i]=URLEncoder.encode(input[i],enc);
        }
        
        StringBuilder url=new StringBuilder("https://open-api.bahn.de/bin/rest.exe/");
        switch(input.length){
            //requesting stations
            case 2:{
                //https://open-api.bahn.de/bin/rest.exe/location.name?authKey=xxx&lang=de&input=ort
                url.append("location.name?authKey=").append(KEY); 
                
                break;
            }
           
            //requesting departures
            default :{
                //https://open-api.bahn.de/bin/rest.exe/departureBoard?authKey=xxx&lang=de&id=xxxx&date=yyyy-mm--dd&time=hh%3amm"
                if(departure){
                    url.append("departureBoard?authKey=").append(KEY);
                }
                else{
                    url.append("arrivalBoard?authKey=").append(KEY);
                }
                break;
            }
        }
            
        //add variable parts of URL
        appendArray(url,input);
        
        //return stream
        return streamFromURL(url.toString());
    }
    
    //appends input information to StringBuilder
    private static void appendArray(StringBuilder str,String [] input){
        
        String lan=input[1];
        //depends on input length
        switch(input.length){
            //requesting stations to input
            case 2:{
                String loc=input[0];
                //https://open-api.bahn.de/bin/rest.exe/location.name?authKey=xxx&lang=de&input=ort
                str.append("&lang=").append(lan).append("&input=").append(loc);
                
                break;
            }
            
            case 3:{
                String id=input[0];
                //last argument is formatted date for request
                //URL-encoder replaces " " with + so replace back again
                String[] splitted= input[2].replace('+',' ').split(" ");
                String date=splitted[0];
                String time=splitted[1];
                
                str.append("&lang=").append(lan).append("&id=").append(id);
                str.append("&date=").append(date).append("&time=").append(time);
                
                break;
            }
        }
    }
    
    //creates connection to url given by the StringBuilder returns content as inputStream
    private static InputStream streamFromURL(String str) throws MalformedURLException, IOException{
        //create url
        URL bahn_url = new URL(str);
        
        //open connection
        URLConnection con = bahn_url.openConnection();
        
        //create reader
        return con.getInputStream();
    } 
    
    
}

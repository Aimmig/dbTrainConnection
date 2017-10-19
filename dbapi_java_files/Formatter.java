/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dbapi;

import static dbapi.DBApi.history;
import java.text.ParseException;
import java.util.Calendar;
import java.util.Date;

/**
 *
 * @author andre
 */
public class Formatter {
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
    
    
}

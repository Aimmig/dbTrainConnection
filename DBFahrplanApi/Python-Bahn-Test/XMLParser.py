#import xml stuff
import xml.etree.ElementTree as ET
#import qt-stuff
from PyQt5 import QtCore as qc
from Stop import Stop
from Connection import Connection

ID='id'
NAME='name'
TYPE='type'
STOPID='stopid'
STOP='stop'
TIME='time'
DATE='date'
ORIGIN='origin'
DIRECTION='direction'
TRACK='track'
REF='ref'
ARRTIME='arrTime'
ARRDATE='arrDate'
DEPTIME='depTime'
DEPDATE='depDate'
LON='lon'
LAT='lat'
STOPS='Stops'

#returns list of name and id of stops from xml-String
def getStationsFromXMLString(xmlString):
        root=ET.fromstring(xmlString)
        #write id and names to temporary variable
        stations=[]
        station_ids=[]
        #iterate over all childs and add attributes to lists
        for child in root:
                station_ids.append(child.attrib[ID])
                stations.append(child.attrib[NAME])
        return (stations,station_ids)        

#converts String formatted as hh:mm to QTime object
def timeStringToQTime(timeString):
        splittedTime=timeString.split(":")
        hours=int(splittedTime[0])
        minutes=int(splittedTime[1])
        time=qc.QTime(hours,minutes)
        return time
    
#converts String formatted as yyyy-mm-dd to QDate object
def dateStringToQDate(dateString):
        splittedDate=dateString.split("-")
        year=int(splittedDate[0])
        month=int(splittedDate[1])
        day=int(splittedDate[2])
        date=qc.QDate(year,month,day)
        return date

def getConnectionsFromXMLString(xmlString,isDeparture):
        try:
                root=ET.fromstring(xmlString)
                #iterate over all connections
                connections=[]
                for con in root:
                        #connection name is mandatory
                        name=con.attrib[NAME]
                        # check if type exist --spelling mistake in xml
                        if TYPE in con.attrib:
                                typ=con.attrib[TYPE]
                        else:
                                typ=""
                        #stop, id and time, date are mandatory
                        stopid=con.attrib[STOPID]
                        stopName=con.attrib[STOP]
                        #convert time and date string to Qt Objects
                        timeString=con.attrib[TIME]
                        time=timeStringToQTime(timeString)
                        dateString=con.attrib[DATE]
                        date=dateStringToQDate(dateString)
                        #read direction if departure
                        if isDeparture and DIRECTION in con.attrib:
                                direction=con.attrib[DIRECTION]
                                origin=""
                        elif not isDeparture and ORIGIN in con.attrib:
                                origin=con.attrib[ORIGIN]
                                direction=""
                        else:
                                origin=""
                                direction=""
                        #track might not be set in xml
                        if TRACK in con.attrib:
                                track=con.attrib[TRACK]
                        else:
                                track=""
                        #read reference link
                        for details in con :
                                if REF in details.attrib:
                                        ref=details.attrib[REF]
                                else:
                                        ref=""
                        #add connection with these information to local list of connections
                        connections.append(Connection   (name,typ,stopid,stopName,time,date,direction,origin,track,ref))
                return connections
        except ET.ParseError  as e:
                return ""

#returns a list of all stops parsed from xmlString
def getStopListFromXMLString(xmlString):
        try:
                #create xml object from string
                root=ET.fromstring(xmlString)
                stopList=[]
                for c in root:
                        if c.tag=="Stops":
                                #iterate over all Stops
                                for child in c:        
                                        #name and id of the station are mandatory         
                                        name=child.attrib[NAME]
                                        identifier=child.attrib[ID]
                                        #departure and arrive time and date might not be set
                                        # convert all times and dates to QDate and QTime objects
                                        if ARRTIME in child.attrib:
                                                arrTimeString=child.attrib[ARRTIME]
                                                arrTime=timeStringToQTime(arrTimeString)
                                        else:
                                                arrTime=""
                                        if ARRDATE in child.attrib:
                                                arrDateString=child.attrib[ARRDATE]
                                                arrDate=dateStringToQDate(arrDateString)
                                        else:
                                                arrDate=""
                                        if DEPTIME in child.attrib:
                                                depTimeString=child.attrib[DEPTIME]
                                                depTime=timeStringToQTime(depTimeString)
                                        else:
                                                depTime=""
                                        if DEPDATE in child.attrib:
                                                depDateString=child.attrib[DEPDATE]
                                                depDate=dateStringToQDate(depDateString)
                                        else:
                                                depDate=""
                                        #track might not be set
                                        if TRACK in child.attrib:
                                                track=child.attrib[TRACK]
                                        else:
                                                track=""
                                        #longitude, latitude are mandatory
                                        lon=child.attrib[LON]
                                        lat=child.attrib[LAT]
                                        #create stop with all these informations
                                        stop=Stop   (name,identifier,arrTime,arrDate,depTime,depDate,track,lon,lat)
                                 #add it to local list
                                        stopList.append(stop)
                #return list of all stops
                return stopList
        except ET.ParseError  as e:
                return ""
  

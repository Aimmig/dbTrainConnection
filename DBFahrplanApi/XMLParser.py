#    -----------------------------------------------------------------------
#    This programm requests connections and corresponding details from the
#    API of Deutsche Bahn and presents them in an user interface
#    This file encapsulates the parsing of the requested xml string into 
#    instances of the data structures.
#    Copyright (C) 2017  Andre Immig, andreimmig@t-online.de
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#    ---------------------------------------------------------------------

#import xml stuff
import xml.etree.ElementTree as ET
#import qt-stuff
from PyQt5 import QtCore as qc
from Structs import Stop
from Structs import Connection

#constansts for parsing xml-Document
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
HOUR_INDEX=0
MINUTE_INDEX=1
YEAR_INDEX=0
MONTH_INDEX=1
DAY_INDEX=2

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
        #splitt String at ':'
        splittedTime=timeString.split(":")
        #convert hours and minutes to int
        hours=int(splittedTime[HOUR_INDEX])
        minutes=int(splittedTime[MINUTE_INDEX])
        #create QTime object
        time=qc.QTime(hours,minutes)
        return time
    
#converts String formatted as yyyy-mm-dd to QDate object
def dateStringToQDate(dateString):
        #splitt String at '-'
        splittedDate=dateString.split("-")
        #convert yeahr, month and day to int
        year=int(splittedDate[YEAR_INDEX])
        month=int(splittedDate[MONTH_INDEX])
        day=int(splittedDate[DAY_INDEX])
        #create QDate object
        date=qc.QDate(year,month,day)
        return date

#returns list of all connections parsed from xmlString
def getConnectionsFromXMLString(xmlString,isDeparture):
        try:
                #load xmlString in element tree
                root=ET.fromstring(xmlString)
                connections=[]
                #iterate over all connections
                for con in root:
                        #connection name is mandatory
                        name=con.attrib[NAME]
                        # check if type exist
                        if TYPE in con.attrib:
                                typ=con.attrib[TYPE]
                        #avoid spelling mistake in xml
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
                        #read direction if is departure and departure exists
                        if isDeparture and DIRECTION in con.attrib:
                                #set direction
                                direction=con.attrib[DIRECTION]
                                origin=""
                        #read origin if is not departure and origin exsits
                        elif not isDeparture and ORIGIN in con.attrib:
                                #set origin
                                origin=con.attrib[ORIGIN]
                                direction=""
                        #invalid case might happen
                        else:
                                #set both attributes to ""
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
                #load xmlString to element Tree
                root=ET.fromstring(xmlString)
                stopList=[]
                #iterate over all childs c
                for c in root:
                        #only use Stop-childs of c
                        if c.tag=="Stops":
                                #iterate over all single Stops
                                for child in c:        
                                        #name and id of the station are mandatory         
                                        name=child.attrib[NAME]
                                        identifier=child.attrib[ID]
                                        #check if arrival time exists
                                        if ARRTIME in child.attrib:
                                                #read arrival time
                                                arrTimeString=child.attrib[ARRTIME]
                                                #convert arrival time to QTime
                                                arrTime=timeStringToQTime(arrTimeString)
                                        else:
                                                arrTime=""
                                        #check if arrival date exists
                                        if ARRDATE in child.attrib:
                                                #read arrivl date
                                                arrDateString=child.attrib[ARRDATE]
                                                #convert arrival date to QDate 
                                                arrDate=dateStringToQDate(arrDateString)
                                        else:
                                                arrDate=""
                                        #check if departure time exists
                                        if DEPTIME in child.attrib:
                                                #read departure Time
                                                depTimeString=child.attrib[DEPTIME]
                                                #convert departure time to QTime
                                                depTime=timeStringToQTime(depTimeString)
                                        else:
                                                depTime=""
                                        #check if departure date exists
                                        if DEPDATE in child.attrib:
                                                #read departure date
                                                depDateString=child.attrib[DEPDATE]
                                                #convert departure date to QDate object
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
  

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

class XMLParser:
        """
        Static class for parsing the requested information out of
        the XML-String and convert it to objects.
        """
        
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
        DATE_FORMAT="yyyy-MM-dd"
        TIME_FORMAT="hh:mm"
        
        @staticmethod
        def getStationsFromXMLString(xmlString):
                """
                Parses the xmlString and returns a list of all stop names
                and a list of all corresponding id's of these stops.
                """
                
                root=ET.fromstring(xmlString)
                #write id and names to temporary variable
                stations=[]
                station_ids=[]
                #iterate over all childs and add attributes to lists
                for child in root:
                        station_ids.append(child.attrib[XMLParser.ID])
                        stations.append(child.attrib[XMLParser.NAME])
                return (stations,station_ids)        

        @staticmethod
        def getConnectionsFromXMLString(xmlString,isDeparture):
                """
                Parses xmlString and returns list of all connections
                contained in the string.
                Takes a boolean flag isDeparture to ensure departure/arrival.
                Returns empty string on parsing error.
                """
                
                try:
                        #load xmlString in element tree
                        root=ET.fromstring(xmlString)
                        connections=[]
                        #iterate over all connections
                        for con in root:
                                #connection name is mandatory
                                name=con.attrib[XMLParser.NAME]
                                # check if type exist
                                if XMLParser.TYPE in con.attrib:
                                        typ=con.attrib[XMLParser.TYPE]
                                #avoid spelling mistake in xml
                                else:
                                        typ=""
                                #stop, id and time, date are mandatory
                                stopid=con.attrib[XMLParser.STOPID]
                                stopName=con.attrib[XMLParser.STOP]
                                #convert time and date string to Qt Objects
                                timeString=con.attrib[XMLParser.TIME]
                                time=qc.QTime.fromString(timeString,XMLParser.TIME_FORMAT)
                                dateString=con.attrib[XMLParser.DATE]
                                date=qc.QDate.fromString(dateString,XMLParser.DATE_FORMAT)
                                #read direction if is departure and departure exists
                                if isDeparture and XMLParser.DIRECTION in con.attrib:
                                        #set direction
                                        direction=con.attrib[XMLParser.DIRECTION]
                                        origin=""
                                #read origin if is not departure and origin exsits
                                elif not isDeparture and XMLParser.ORIGIN in con.attrib:
                                        #set origin
                                        origin=con.attrib[XMLParser.ORIGIN]
                                        direction=""
                                #invalid case might happen
                                else:
                                        #set both attributes to ""
                                        origin=""
                                        direction=""
                                #track might not be set in xml
                                if XMLParser.TRACK in con.attrib:
                                        track=con.attrib[XMLParser.TRACK]
                                else:
                                        track=""
                                #read reference link
                                for details in con :
                                        if XMLParser.REF in details.attrib:
                                                ref=details.attrib[XMLParser.REF]
                                        else:
                                                ref=""
                                #add connection with these information to local list of connections
                                connections.append(Connection(name,typ,stopid,stopName,time,date,direction,origin,track,ref))
                        return connections
                except ET.ParseError  as e:
                        return ""

        @staticmethod
        def getStopListFromXMLString(xmlString):
                """
                Parses xmlString and returns list of all stops of a connection
                contained in the string.
                Returns empty string on parsing error.
                """
                
                try:
                        #load xmlString to element Tree
                        root=ET.fromstring(xmlString)
                        stopList=[]
                        #iterate over all childs c
                        for c in root:
                                #only use Stop-childs of c
                                if c.tag==XMLParser.STOPS:
                                        #iterate over all single Stops
                                        for child in c:        
                                                #name and id of the station are mandatory         
                                                name=child.attrib[XMLParser.NAME]
                                                identifier=child.attrib[XMLParser.ID]
                                                #check if arrival time exists
                                                if XMLParser.ARRTIME in child.attrib:
                                                        #read arrival time
                                                        arrTimeString=child.attrib[XMLParser.ARRTIME]
                                                        #convert arrival time to QTime
                                                        arrTime=qc.QTime.fromString(arrTimeString,XMLParser.TIME_FORMAT)
                                                else:
                                                        arrTime=""
                                                #check if arrival date exists
                                                if XMLParser.ARRDATE in child.attrib:
                                                        #read arrivl date
                                                        arrDateString=child.attrib[XMLParser.ARRDATE]
                                                        #convert arrival date to QDate 
                                                        arrDate=qc.QDate.fromString(arrDateString,XMLParser.DATE_FORMAT)
                                                else:
                                                        arrDate=""
                                                #check if departure time exists
                                                if XMLParser.DEPTIME in child.attrib:
                                                        #read departure Time
                                                        depTimeString=child.attrib[XMLParser.DEPTIME]
                                                        #convert departure time to QTime
                                                        depTime=qc.QTime.fromString(depTimeString,XMLParser.TIME_FORMAT)
                                                else:
                                                        depTime=""
                                                #check if departure date exists
                                                if XMLParser.DEPDATE in child.attrib:
                                                        #read departure date
                                                        depDateString=child.attrib[XMLParser.DEPDATE]
                                                        #convert departure date to QDate object
                                                        depDate=qc.QDate.fromString(depDateString,XMLParser.DATE_FORMAT)
                                                else:
                                                        depDate=""
                                                #track might not be set
                                                if XMLParser.TRACK in child.attrib:
                                                        track=child.attrib[XMLParser.TRACK]
                                                else:
                                                        track=""
                                                #longitude, latitude are mandatory
                                                lon=child.attrib[XMLParser.LON]
                                                lat=child.attrib[XMLParser.LAT]
                                                #create stop with all these informations
                                                stop=Stop   (name,identifier,arrTime,arrDate,depTime,depDate,track,lon,lat)
                                                #add it to local list
                                                stopList.append(stop)
                        #return list of all stops
                        return stopList
                except ET.ParseError  as e:
                        return ""

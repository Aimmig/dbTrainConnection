#import xml stuff
import xml.etree.ElementTree as ET
#import qt-stuff
from PyQt5 import QtCore as qc
from Stop import Stop
from Connection import Connection

#returns list of name and id of stops from xml-String
def getStationsFromXMLString(xmlString):
        root=ET.fromstring(xmlString)
        #write id and names to temporary variable
        stations=[]
        station_ids=[]
        #iterate over all childs and add attributes to lists
        for child in root:
                station_ids.append(child.attrib['id'])
                stations.append(child.attrib['name'])
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
        root=ET.fromstring(xmlString)
        #iterate over all connections
        connections=[]
        for con in root:
                #connection name is mandatory
                name=con.attrib['name']
                # check if type exist --spelling mistake in xml
                if 'type' in con.attrib:
                        typ=con.attrib['type']
                else:
                        typ=""
                #stop, id and time, date are mandatory
                stopid=con.attrib['stopid']
                stopName=con.attrib['stop']
                #convert time and date string to Qt Objects
                timeString=con.attrib['time']
                time=timeStringToQTime(timeString)
                dateString=con.attrib['date']
                date=dateStringToQDate(dateString)
                #read direction if departure
                if isDeparture and 'direction' in con.attrib:
                        direction=con.attrib['direction']
                        origin=""
                elif not isDeparture and 'origin' in con.attrib:
                        origin=con.attrib['origin']
                        direction=""
                else:
                        origin=""
                        direction=""
                #track might not be set in xml
                if 'track' in con.attrib:
                        track=con.attrib['track']
                else:
                        track=""
                #read reference link
                for details in con :
                        if 'ref' in details.attrib:
                                ref=details.attrib['ref']
                        else:
                                ref=""
                #add connection with these information to local list of connections
                connections.append(Connection(name,typ,stopid,stopName,time,date,direction,origin,track,ref))
        return connections

#returns a list of all stops parsed from xmlString
def getStopListFromXMLString(xmlString):
        #create xml object from string
        root=ET.fromstring(xmlString)
        stopList=[]
        for c in root:
                if c.tag=="Stops":
                        #iterate over all Stops
                        for child in c:        
                                #name and id of the station are mandatory         
                                name=child.attrib['name']
                                identifier=child.attrib['id']
                                #departure and arrive time and date might not be set
                                # convert all times and dates to QDate and QTime objects
                                if 'arrTime' in child.attrib:
                                        arrTimeString=child.attrib['arrTime']
                                        arrTime=timeStringToQTime(arrTimeString)
                                else:
                                        arrTime=""
                                if 'arrDate' in child.attrib:
                                        arrDateString=child.attrib['arrDate']
                                        arrDate=dateStringToQDate(arrDateString)
                                else:
                                        arrDate=""
                                if 'depTime' in child.attrib:
                                        depTimeString=child.attrib['depTime']
                                        depTime=timeStringToQTime(depTimeString)
                                else:
                                        depTime=""
                                if 'depDate' in child.attrib:
                                        depDateString=child.attrib['depDate']
                                        depDate=dateStringToQDate(depDateString)
                                else:
                                        depDate=""
                                #track might not be set
                                if 'track' in child.attrib:
                                        track=child.attrib['track']
                                else:
                                        track=""
                                #longitude, latitude are mandatory
                                lon=child.attrib['lon']
                                lat=child.attrib['lat']
                                #create stop with all these informations
                                stop=Stop   (name,identifier,arrTime,arrDate,depTime,depDate,track,lon,lat)
                                #add it to local list
                                stopList.append(stop)
        #return list of all stops
        return stopList
  

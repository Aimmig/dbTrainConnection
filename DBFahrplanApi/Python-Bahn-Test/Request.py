import urllib.request as url_req
import urllib.error as err
from PyQt5 import QtCore as qc

KEY="DBhackFrankfurt0316"
GOOGLEMAPS_KEY="AIzaSyAa0JAwUZMPl5DbBuUn6IRCzh9PKGGtFx4"
LANGUAGE="de"
DB_BASE_URL="https://open-api.bahn.de/bin/rest.exe/"
GOOGLE_MAPS_BASE_URL="https://maps.googleapis.com/maps/api/staticmap?"
MAP_WIDTH="800"
MAP_HEIGHT="800"
PATH_COLOR="0xff000088"
MARKER_COLOR="0x5555BB"
MARKER_SIZE="small"
MARKER_COLOR_SPECIAL="0xaa339988"
MARKER_SIZE_SPECIAL="mid"
PATH_SIZE="3"

#returns the XML-String 
def getXMLStringConnectionDetails(urlString):
        req=url_req.Request(urlString)
        try:
            with url_req.urlopen(req) as response:
                result=response.read()
                return result
        except err.HTTPError as e:
             print('The server couldn\'t fulfill the request.')
             print('Error code: ', e.code)
        except err.URLError as e:
             print('We failed to reach a server.')
             print('Reason: ', e.reason)
        return ""
        

#returns the XML-String representation of the requested ressource
def getXMLStringStationRequest(loc):
        url=createStationRequestURL(loc)
        req=url_req.Request(url)
        try:
            with url_req.urlopen(req) as response:
                result=response.read()
                return result
        except err.HTTPError as e:
             print('The server couldn\'t fulfill the request.')
             print('Error code: ', e.code)
        except err.URLError as e:
             print('We failed to reach a server.')
             print('Reason: ', e.reason)
        return ""

#returns the XML-String representation of the Connection Request
def getXMLStringConnectionRequest(date,time,identifier,isDeparture):
        url=createConnectionRequestURL(date,time,identifier,isDeparture)
        print(url)
        req=url_req.Request(url)
        try:
            with url_req.urlopen(req) as response:
                result=response.read()
                return result
        except err.HTTPError as e:
             print('The server couldn\'t fulfill the request.')
             print('Error code: ', e.code)
        except err.URLError as e:
             print('We failed to reach a server.')
             print('Reason: ', e.reason)
        return ""

def getMapWithLocations(coordinates,markerIndex):
        url=createMapURL(coordinates,markerIndex)
        req=url_req.Request(url)
        return url_req.urlopen(req).read() 

#creates the URL for requesting Connections
def createConnectionRequestURL(date,time,identifier,isDeparture):
        #build date-String
        dateString=str(date.year())+"-"+str(date.month())+"-"+str(date.day())
        #print(date.toString("yyyy-M-d"))
        #build and encode timeString
        timeString=str(time.hour())+"%3A"+str(time.minute())
        #print(timeString)
        #print(time.toString("h:m").replace(":","%3A"))
        #build last part of url
        lastPart="authKey="+KEY+"&lang="+LANGUAGE+"&id="
        lastPart=lastPart+str(identifier)+"&date="+dateString+"&time="+timeString
        #build complete url
        if isDeparture:
             return DB_BASE_URL+"departureBoard?"+lastPart
        else:
             return DB_BASE_URL+"arrivalBoard?"+lastPart

#creates the URL for requesting Stations
def createStationRequestURL(loc):
        return DB_BASE_URL+"location.name?authKey="+KEY+"&lang="+LANGUAGE+"&input="+loc

#creates URL  for requesting the map with path of given locations and lat lon for marker
def createMapURL(coordinates,markerIndex):
        res=GOOGLE_MAPS_BASE_URL+"&size="+MAP_WIDTH+"x"+MAP_HEIGHT+"&language="+LANGUAGE        
        res+="&sensor=false&path=color:"+PATH_COLOR+"|weight:"+PATH_SIZE
        for loc in coordinates:
                res+="|"+str(loc.lat)+","+str(loc.lon)
        res+="&markers=size:"+MARKER_SIZE_SPECIAL+"|color:"+MARKER_COLOR_SPECIAL+"|"
        res+=str(coordinates[markerIndex].lat)+","+str(coordinates[markerIndex].lon)
        del coordinates[markerIndex]
        res+="&markers=size:"+MARKER_SIZE+"|color:"+MARKER_COLOR+"|"
        for loc in coordinates:
                res+="|"+str(loc.lat)+","+str(loc.lon)
        res+="&key="+GOOGLEMAPS_KEY
        return res

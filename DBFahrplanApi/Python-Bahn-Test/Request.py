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
PATH_SIZE="3"
LAT_INDEX=0
LON_INDEX=1

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

def getMapWithLocations(coordinates):
        url=createMapURL(coordinates)
        req=url_req.Request(url)
        return url_req.urlopen(req).read() 

#creates the URL for requesting Connections
def createConnectionRequestURL(date,time,identifier,isDeparture):
        #build date-String
        dateString=str(date.year())+"-"+str(date.month())+"-"+str(date.day())
        #build and encode timeString
        timeString=str(time.hour())+"%3A"+str(time.minute())
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

#creates URL  for requesting the map with path of given locations
def createMapURL(coordinates):
        res=GOOGLE_MAPS_BASE_URL+"&size="+MAP_WIDTH+"x"+MAP_HEIGHT+"&language="+LANGUAGE+"&sensor=false&path=color:"+PATH_COLOR+"|weight:"+PATH_SIZE
        for loc in coordinates:
                res+="|"+str(loc[LAT_INDEX])+","+str(loc[LON_INDEX])
        res+="&key="+GOOGLEMAPS_KEY
        return res

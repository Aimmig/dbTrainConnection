# -*- coding: utf-8 -*-

import urllib.request as url_req
import urllib.error as err
import urllib.parse as parse
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg

KEY="DBhackFrankfurt0316"
GOOGLEMAPS_KEY="AIzaSyAa0JAwUZMPl5DbBuUn6IRCzh9PKGGtFx4"
LANGUAGE="de"
DB_BASE_URL="https://open-api.bahn.de/bin/rest.exe/"
GOOGLE_MAPS_BASE_URL="https://maps.googleapis.com/maps/api/staticmap?"
DATE_FORMAT="yyyy-M-d"
TIME_FORMAT="h:m"
ENCODED_SEPERATOR="%3A"

class Request:
        #returns the XML-String
        @staticmethod
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
        @staticmethod
        def getXMLStringStationRequest(loc):
                url=Request.createStationRequestURL(loc)
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
        @staticmethod
        def getXMLStringConnectionRequest(date,time,identifier,isDeparture):
                url=Request.createConnectionRequestURL(date,time,identifier,isDeparture)
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

        @staticmethod
        def getMapWithLocations(coordinates,markerIndex,settings):
                url=Request.createMapURL(coordinates,markerIndex,settings)
                req=url_req.Request(url)
                return url_req.urlopen(req).read() 

        @staticmethod
        #creates the URL for requesting Connections
        def createConnectionRequestURL(date,time,identifier,isDeparture):
                #build date-String
                dateString=date.toString(DATE_FORMAT)
                #build and encode timeString
                timeString=time.toString(TIME_FORMAT).replace(":",ENCODED_SEPERATOR)
                #build last part of url
                lastPart="authKey="+KEY+"&lang="+LANGUAGE+"&id="
                lastPart=lastPart+str(identifier)+"&date="+dateString+"&time="+timeString
                #build complete url
                if isDeparture:
                        return DB_BASE_URL+"departureBoard?"+lastPart
                else:
                        return DB_BASE_URL+"arrivalBoard?"+lastPart

        #creates the URL for requesting Stations
        @staticmethod
        def createStationRequestURL(loc):
                return DB_BASE_URL+"location.name?authKey="+KEY+"&lang="+LANGUAGE+"&input="+parse.quote(loc.replace(" ",""))

        #creates URL  for requesting the map with path of given locations and lat lon for marker
        @staticmethod
        def createMapURL(coordinates,markerIndex,settings):
                res=GOOGLE_MAPS_BASE_URL+"&size="+str(settings.width)+"x"+str(settings.height)+"&language="+LANGUAGE        
                res+="&sensor=false&path=color:"+settings.formatPathColor()+"|weight:"+settings.PATH_SIZE
                for loc in coordinates:
                        res+="|"+str(loc.lat)+","+str(loc.lon)
                res+="&markers=size:"+settings.MARKER_SIZE_SPECIAL+"|color:"+settings.formatSpecialColor()+"|"
                res+=str(coordinates[markerIndex].lat)+","+str(coordinates[markerIndex].lon)
                del coordinates[markerIndex]
                res+="&markers=size:"+settings.MARKER_SIZE+"|color:"+settings.formatColor()+"|"
                for loc in coordinates:
                        res+="|"+str(loc.lat)+","+str(loc.lon)
                res+="&key="+GOOGLEMAPS_KEY
                return res

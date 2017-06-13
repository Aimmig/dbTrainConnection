#    -----------------------------------------------------------------------
#    This programm requests connections and corresponding details from the
#    API of Deutsche Bahn and presents them in an user interface
#    This file encapsulates the logic for actually requesting the connection and
#    their details from the API as well as requesting a coresponding map from 
#    Google-Maps-Static API.
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

import urllib.request as url_req
import urllib.error as err
import urllib.parse as parse
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg

#API-Keys
KEY="DBhackFrankfurt0316"
GOOGLEMAPS_KEY="AIzaSyAa0JAwUZMPl5DbBuUn6IRCzh9PKGGtFx4"
#language of Request
LANGUAGE="de"
#API base urls
DB_BASE_URL="https://open-api.bahn.de/bin/rest.exe/"
GOOGLE_MAPS_BASE_URL="https://maps.googleapis.com/maps/api/staticmap?"
#format strings for time and date
DATE_FORMAT="yyyy-M-d"
TIME_FORMAT="h:m"
ENCODED_SEPERATOR="%3A"

#static class for handling request
class Request:

        #establishes connection with server and reads result
        @staticmethod
        def getResultFromServer(url):
                req=url_req.Request(url)
                response=url_req.urlopen(req)
                result=response.read()
                return result

        #returns the XML-String requested from the given urlString
        @staticmethod
        def getXMLStringConnectionDetails(url):
                return Request.getResultFromServer(url)

        #returns the XML-String representation of the requested ressource
        @staticmethod
        def getXMLStringStationRequest(loc):
                url=Request.createStationRequestURL(loc)
                return Request.getResultFromServer(url)

        #returns the XML-String representation of the Connection Request
        @staticmethod
        def getXMLStringConnectionRequest(date,time,identifier,isDeparture):
                url=Request.createConnectionRequestURL(date,time,identifier,isDeparture)
                return Request.getResultFromServer(url)

        #request map with given settings and cooridnates and returns it as raw data
        @staticmethod
        def getMapWithLocations(coordinates,markerIndex,settings):
                #create url with settings
                url=Request.createMapURL(coordinates,markerIndex,settings)
                return Request.getResultFromServer(url)

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
                #add width and heigt and language of map to base url
                res=GOOGLE_MAPS_BASE_URL+"&size="+str(settings.width)+"x"+str(settings.height)+"&language="+LANGUAGE  
                #add path color and size to url      
                res+="&sensor=false&path=color:"+settings.formatPathColor()+"|weight:"+settings.PATH_SIZE
                #add string of all coordinates for path
                res+=Request.createFullCoordinateString(coordinates)
                #add special marker size and color to url
                res+="&markers=size:"+settings.MARKER_SIZE_SPECIAL+"|color:"+settings.formatSpecialColor()
                #add String of special cordinate for special marker
                res+=Request.createCoordinateString(coordinates[markerIndex])
                #delete special element it should not be marked 2 times
                del coordinates[markerIndex]
                #add marker size and color for normal locations
                res+="&markers=size:"+settings.MARKER_SIZE+"|color:"+settings.formatColor()+"|"
                #add string of all coordinates for markers
                res+=Request.createFullCoordinateString(coordinates)
                #add googlemapskey
                res+="&key="+GOOGLEMAPS_KEY
                return res
        
        #create formated coordinate String
        @staticmethod
        def createFullCoordinateString(cords):
                res=""
                #iterate over all locations
                for loc in cords:
                        #add representation for loc
                        res+=Request.createCoordinateString(loc)
                return res

        #create representation of one location
        @staticmethod
        def createCoordinateString(loc):
                #single coordinate is formatted to |lat,lon
                return "|"+str(loc.lat)+","+str(loc.lon)

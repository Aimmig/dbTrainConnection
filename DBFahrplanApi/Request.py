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

class Request:
        """
        Class to encapsulate the requests of a ressource and
        the creation of the corresponding urls used as ressource.
        """
        
        #static member variables
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

        @staticmethod
        def getResultFromServer(url):
                """
                Establishes connection to the given url, reads and returns
                the result of this ressource.
                """
                
                req=url_req.Request(url)
                response=url_req.urlopen(req)
                result=response.read()
                return result

        @staticmethod
        def getXMLStringConnectionDetails(url):
                """
                Returns the result of the given url ressource.
                Used for requesting the connection details from the reference link.
                """
                
                return Request.getResultFromServer(url)

        @staticmethod
        def getXMLStringStationRequest(loc):
                """
                Creates url for requesting all locations that match to the given
                location loc.
                Request these locations and returns the XML-String.
                """
                
                url=Request.createStationRequestURL(loc)
                return Request.getResultFromServer(url)

        @staticmethod
        def getXMLStringConnectionRequest(date,time,identifier,isDeparture):
                """
                Creates url for requesting connections from date,time,
                identifier (corresponding to a location) and a boolean departure
                flag variable.
                Request the connections and returns the XML-String.
                """
                
                url=Request.createConnectionRequestURL(date,time,identifier,isDeparture)
                return Request.getResultFromServer(url)

        @staticmethod
        def getMapWithLocations(coordinates,markerIndex,settings):
                """
                Creates google-maps url for corresponding map with given coordinates and settings.
                Returns the raw requested data.
                """
                
                url=Request.createMapURL(coordinates,markerIndex,settings)
                return Request.getResultFromServer(url)

        @staticmethod
        def createConnectionRequestURL(date,time,identifier,isDeparture):
                """
                Builds and returns the url for requesting connection from date,time,
                identifier (corresponding to a location) and a boolean departure
                flag variable.
                """
                
                #build date-String
                dateString=date.toString(Request.DATE_FORMAT)
                #build and encode timeString
                timeString=time.toString(Request.TIME_FORMAT).replace(":",Request.ENCODED_SEPERATOR)
                #build last part of url
                lastPart="authKey="+Request.KEY+"&lang="+Request.LANGUAGE+"&id="
                lastPart=lastPart+str(identifier)+"&date="+dateString+"&time="+timeString
                #build complete url
                if isDeparture:
                        return Request.DB_BASE_URL+"departureBoard?"+lastPart
                else:
                        return Request.DB_BASE_URL+"arrivalBoard?"+lastPart

        @staticmethod
        def createStationRequestURL(loc):
                """
                Builds and returns the url for requesting all locations that match to the
                given location loc.
                """
                
                return Request.DB_BASE_URL+"location.name?authKey="+Request.KEY+"&lang="+Request.LANGUAGE+"&input="+parse.quote(loc.replace(" ",""))

        @staticmethod
        def createMapURL(coordinates,markerIndex,settings):
                """
                Builds and returns the url for requesting the map with coordinates and settings.
                Use size, path- and marker color from settings.
                Create full path with all coordinates, for each coordinate add marker with
                default size except the specified markerIndex, these coordinate gets an other
                color specified in settings.
                """
                
                #add width and heigt and language of map to base url
                res=Request.GOOGLE_MAPS_BASE_URL+"&size="+str(settings.width)+"x"+str(settings.height)+"&language="+Request.LANGUAGE  
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
                res+="&key="+Request.GOOGLEMAPS_KEY
                return res
        
        @staticmethod
        def createFullCoordinateString(cords):
                """
                Takes a list of geographical locations and returns a string
                that is formatted for use in google-maps request.
                """
                
                res=""
                #iterate over all locations
                for loc in cords:
                        #add representation for loc
                        res+=Request.createCoordinateString(loc)
                return res

        @staticmethod
        def createCoordinateString(loc):
                """
                Takes a geographical location and returns a string
                that is formatted for use in google-maps request.
                """
                
                #single coordinate is formatted to |lat,lon
                return "|"+str(loc.lat)+","+str(loc.lon)

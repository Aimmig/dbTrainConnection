#    -----------------------------------------------------------------------
#    This program requests connections and corresponding details from the
#    API of Deutsche Bahn and presents them in an user interface
#    This file encapsulates the logic for actually requesting the connection and
#    their details from the API as well as requesting a corresponding map from
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

from PyQt5 import QtCore
import urllib.request as url_req
import urllib.parse as parse
from Structs import Coordinate, RequestSettings, MapType


class Request:
    """
    Class to encapsulate the requests of a resource and
    the creation of the corresponding urls used as resource.
    """

    # static member variables
    # API base urls
    DB_BASE_URL = 'https://open-api.bahn.de/bin/rest.exe/'
    GOOGLE_MAPS_BASE_URL = 'https://maps.googleapis.com/maps/api/staticmap?'
    EncodedSeparator = '%3A'

    # API-Properties key-words for Deutsche Bahn API
    UrlLang = '&lang='
    UrlDate = '&date='
    UrlTime = '&time='
    UrlId = '&id='
    UrlAuthKey = 'authKey='
    UrlLocationName = 'location.name?'
    UrlDepBoard = 'departureBoard?'
    UrlArrBoard = 'arrivalBoard?'
    UrlInput = '&input='

    # API-Properties key-words for Google-Maps static API
    UrlScale = '&scale='
    UrlScaleValue = str(1)
    UrlSensor = '&sensor='
    UrlSensorValue = 'False'
    UrlPathColor = '&path=color:'
    UrlColor = '|color:'
    UrlKey = '&key='
    UrlMarkerSize = '&markers=size:'
    UrlSeparator = '|'
    UrlLanguage = '&language='
    UrlSize = '&size='
    UrlWeight = '|weight:'
    UrlMapType = '&maptype='

    # format strings for time and date
    DATE_FORMAT = 'yyyy-M-d'
    TIME_FORMAT = 'h:m'

    @staticmethod
    def getResultFromServer(url: str) -> str:
        """
        Establishes connection to the given url, reads and returns
        the result of this resource.
        :type url: str
        :rtype str
        """

        req = url_req.Request(url)
        response = url_req.urlopen(req)
        result = response.read()
        return result

    @staticmethod
    def getXMLStringConnectionDetails(url: str) -> str:
        """
        Returns the result of the given url resource.
        Used for requesting the connection details from the reference link.
        :type url str
        :rtype str
        """

        return Request.getResultFromServer(url)

    @staticmethod
    def getXMLStringStationRequest(loc: str, settings: RequestSettings) -> str:
        """
        Creates url for requesting all locations that match to the given
        location loc.
        Request these locations and returns the XML-String.
        :type loc str
        :type settings RequestSettings
        :rtype str
        """

        url = Request.createStationRequestURL(loc, settings)
        return Request.getResultFromServer(url)

    @staticmethod
    def getXMLStringConnectionRequest(date: QtCore.QDate, time: QtCore.QTime, identifier: int,
                                      isDeparture: bool, settings: RequestSettings) -> str:
        """
        Creates url for requesting connections from date,time,
        identifier (corresponding to a location) and a boolean departure
        flag variable.
        Request the connections and returns the XML-String.
        :type date QtCore.QDate
        :type time Qt.Core.QTime
        :type identifier int
        :type isDeparture bool
        :type settings RequestSettings
        :rtype str
        """

        url = Request.createConnectionRequestURL(date, time, identifier, isDeparture, settings)
        return Request.getResultFromServer(url)

    @staticmethod
    def getMapWithLocations(coordinates: [Coordinate], markerIndex: int, settings: RequestSettings) -> str:
        """
        Creates google-maps url for corresponding map with given coordinates and settings.
        Returns the raw requested data
        :type coordinates [Coordinate]
        :type markerIndex int
        :type settings RequestSettings
        :rtype str
        """

        url = Request.createMapURL(coordinates, markerIndex, settings)
        return Request.getResultFromServer(url)

    @staticmethod
    def createConnectionRequestURL(date: QtCore.QDate, time: QtCore.QTime, identifier: int, isDeparture: bool,
                                   settings: RequestSettings) -> str:
        """
        Builds and returns the url for requesting connection from date,time,
        identifier (corresponding to a location) and a boolean departure
        flag variable.
        :type date QtCore.QDate
        :type time Qt.Core.QTime
        :type identifier int
        :type isDeparture bool
        :type settings RequestSettings
        :rtype str

        """
        # build date-String
        dateString = date.toString(Request.DATE_FORMAT)
        # build and encode timeString
        timeString = time.toString(Request.TIME_FORMAT).replace(":", Request.EncodedSeparator)
        # build last part of url
        lastPart = Request.UrlAuthKey + settings.DBKey + Request.UrlLang + settings.LANGUAGE + Request.UrlId
        lastPart = lastPart + str(identifier) + Request.UrlDate + dateString + Request.UrlTime + timeString
        # build complete url
        if isDeparture:
            return Request.DB_BASE_URL + Request.UrlDepBoard + lastPart
        else:
            return Request.DB_BASE_URL + Request.UrlArrBoard + lastPart

    @staticmethod
    def createStationRequestURL(loc: str, settings: RequestSettings) -> str:
        """
        Builds and returns the url for requesting all locations that match to the
        given location loc.
        :type loc str
        :type settings RequestSettings
        :rtype str
        """

        base = '{0}{1}{2}{3}{4}x{5}{6}{7}'
        return base.format(Request.DB_BASE_URL, Request.UrlLocationName, Request.UrlAuthKey, settings.DBKey,
                           Request.UrlLanguage, settings.LANGUAGE, Request.UrlInput, parse.quote(loc.replace(" ", ""))
                           )

    @staticmethod
    def createMapURL(coordinates: [Coordinate], markerIndex: int, settings: RequestSettings) -> str:
        """
        Builds and returns the url for requesting the map with coordinates and settings.
        Use size, path- and marker color from settings.
        Create full path with all coordinates, for each coordinate add marker with
        default size except the specified markerIndex, these coordinate gets an other
        color specified in settings
        :type coordinates [Coordinate]
        :type markerIndex int
        :type settings RequestSettings
        :rtype str
        """

        # add width and height and language of map to base url
        res = Request.GOOGLE_MAPS_BASE_URL + Request.UrlScale + Request.UrlScaleValue + Request.UrlSize + str(settings.width) + 'x' + str(settings.height) + Request.UrlLanguage + settings.LANGUAGE
        # add path color and size to url
        res += Request.UrlSensor + Request.UrlSensorValue + Request.UrlPathColor + settings.formatPathColor() + Request.UrlWeight + settings.PATH_SIZE
        # add string of all coordinates for path
        res += Request.createFullCoordinateString(coordinates)
        # check for valid markerIndex
        if markerIndex >= 0:
            # add special marker size and color to url
            res += Request.UrlMarkerSize + settings.MARKER_SIZE_SPECIAL
            res += Request.UrlColor + settings.formatSpecialColor()
            # add String of special coordinate for special marker
            res += Request.createCoordinateString(coordinates[markerIndex])
            # delete special element it should not be marked 2 times
            del coordinates[markerIndex]
        # add marker size and color for normal locations
        res += Request.UrlMarkerSize + settings.MARKER_SIZE
        res += Request.UrlColor + settings.formatColor() + Request.UrlSeparator
        # add string of all coordinates for markers
        res += Request.createFullCoordinateString(coordinates)
        # add maptype
        res += Request.UrlMapType + MapType(settings.MAPTYPE).name
        # add google map key
        res += Request.UrlKey + settings.GoogleMapsKey
        return res

    @staticmethod
    def createFullCoordinateString(cords: [Coordinate]) -> str:
        """
        Takes a list of geographical locations and returns a string
        that is formatted for use in google-maps request.
        :type cords [Coordinate]
        :rtype str
        """

        return ''.join(map(lambda loc: Request.createCoordinateString(loc), cords))

    @staticmethod
    def createCoordinateString(loc: Coordinate) -> str:
        """
        Takes a geographical location and returns a string
        that is formatted for use in google-maps request.
        :type loc Coordinate
        :rtype str
        """

        # single coordinate is formatted to |lat,lon
        return '{0}{1},{2}'.format(Request.UrlSeparator, str(loc.lat), str(loc.lon))

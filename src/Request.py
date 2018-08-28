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
import urllib.parse as parse
from Structs import RequestSettings, MapType
import requests
import polyline


class Request:
    """
    Class to encapsulate the requests of a resource and
    the creation of the corresponding urls used as resource.
    """

    # static member variables
    # API base urls
    DB_BASE_URL = 'https://open-api.bahn.de/bin/rest.exe/'
    MAPS_BASE_URL = 'https://api.mapbox.com/styles/v1/mapbox/{0}/static/'
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

    # format strings for time and date
    DATE_FORMAT = 'yyyy-M-d'
    TIME_FORMAT = 'h:m'

    @staticmethod
    def formatColor(col):
        """
        Formats given color to be able to use it in web-url
        :param col:
        :return: str
        """
        return col.name().replace('#', '')

    @staticmethod
    def getResultFromServer(url: str) -> str:
        """
        Establishes connection to the given url, reads and returns
        the result of this resource.
        :type url: str
        :rtype str
        """

        hdrs = {'User-Agent': 'Mozilla / 5.0'}
        resp = requests.get(url, headers=hdrs)
        return resp.content

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
                                      isDeparture: bool, settings: RequestSettings) -> (str, str):
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
        :rtype (str,str)
        """

        url = Request.createConnectionRequestURL(date, time, identifier, isDeparture, settings)
        return Request.getResultFromServer(url), url

    @staticmethod
    def regetXMLStringConnectionRequest(url: str, isDeparture: bool):
        if isDeparture:
            new_url = url.replace(Request.UrlArrBoard, Request.UrlDepBoard)
        else:
            new_url = url.replace(Request.UrlDepBoard, Request.UrlArrBoard)
        return Request.getResultFromServer(new_url), new_url

    @staticmethod
    def getMapWithLocations(coordinates: [tuple], markerIndex: int, settings: RequestSettings) -> str:
        """
        Creates google-maps url for corresponding map with given coordinates and settings.
        Returns the raw requested data
        :type coordinates [tuple]
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

        base = '{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}'
        # build last part of url
        lastPart = base.format(Request.UrlAuthKey, settings.DBKey, Request.UrlLang, settings.LANGUAGE, Request.UrlId,
                               str(identifier), Request.UrlDate, dateString, Request.UrlTime, timeString
                               )
        # build complete url
        base = '{0}{1}{2}'
        if isDeparture:
            return base.format(Request.DB_BASE_URL, Request.UrlDepBoard, lastPart)
        else:
            return base.format(Request.DB_BASE_URL, Request.UrlArrBoard, lastPart)

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
                           Request.UrlLang, settings.LANGUAGE, Request.UrlInput, parse.quote(loc.replace(" ", ""))
                           )

    @staticmethod
    def createMapURL(coordinates: [tuple], markerIndex: int, settings: RequestSettings) -> str:
        """
        Builds and returns the url for requesting the map with coordinates and settings.
        Use size, path- and marker color from settings.
        Create full path with all coordinates, for each coordinate add marker with
        default size except the specified markerIndex, these coordinate gets an other
        color specified in settings
        :type coordinates [tuple]
        :type markerIndex int
        :type settings RequestSettings
        :rtype str
        """

        res = Request.MAPS_BASE_URL.format(MapType(settings.MAPTYPE).name).replace('_', '-')
        poly = polyline.encode([(y, x) for x, y in coordinates])
        path = 'path-{0}+{1}-{2}({3}),'.format(settings.PATH_SIZE, Request.formatColor(settings.PATH_COLOR),
                                               settings.PATH_OPACITY, poly)
        endpart = '/auto/{0}x{1}?access_token={2}'.format(str(settings.width), str(settings.height), settings.MapBoxKey)
        res += path + Request.createFullCoordinateString(markerIndex, coordinates, settings) + endpart
        print(res)
        return res

    @staticmethod
    def createFullCoordinateString(markerIndex: int, cords: [tuple], settings) -> str:
        """
        Takes a list of geographical locations and returns a string
        that is formatted for use in google-maps request.
        :type markerIndex int
        :type cords [tuple]
        :type settings RequestSettings
        :rtype str
        """

        col = Request.formatColor(settings.MARKER_COLOR)
        res = ''.join(map(lambda j: Request.createCoordinateStringLabel(col, j + 1, settings.MARKER_SIZE, cords[j]),
                          [i for i in range(len(cords)) if i != markerIndex]))
        return res + (Request.createCoordinateStringLabel(Request.formatColor(settings.MARKER_COLOR_SPECIAL),
                                                          markerIndex + 1, settings.MARKER_SIZE_SPECIAL,
                                                          cords[markerIndex]))[:-1]
        # res =  ''.join(map(lambda j: Request.createCoordinateString(col, settings.MARKER_SIZE, cords[j]),
        #                           [i for i in range(len(cords)) if i != markerIndex]))
        # return res + (Request.createCoordinateString(Request.formatColor(settings.MARKER_COLOR_SPECIAL),
        #                                                   settings.MARKER_SIZE_SPECIAL,
        #                                                   cords[markerIndex]))[:-1]

    @staticmethod
    def createCoordinateStringLabel(col: str, label: int, size: str, loc: tuple) -> str:
        """
        Takes a geographical location and returns a string
        that is formatted for use in google-maps request.
        :type col str
        :type label int
        :type size: str
        :type loc tuple
        :rtype str
        """

        # single marker formated as pin-size-name+color(lon,lat)
        return 'pin-{0}-{1}+{2}{3},'.format(size, label, col, str(loc).replace(' ', ''))

    @staticmethod
    def createCoordinateString(col: str, size: str, loc: tuple) -> str:
        """
        Takes a geographical location and returns a string
        that is formatted for use in google-maps request.
        :type col str
        :type size: str
        :type loc tuple
        :rtype str
        """

        # single marker formated as pin-size-name+color(lon,lat)
        return 'pin-{0}+{1}{2},'.format(size, col, str(loc).replace(' ', ''))

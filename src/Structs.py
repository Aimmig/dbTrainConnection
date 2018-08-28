#    -----------------------------------------------------------------------
#    This program requests connections and corresponding details from the
#    API of Deutsche Bahn and presents them in an user interface.
#    This file encapsulates the most important data structures for saving
#    the requested information, as well as data structures for filtering
#    and saving user settings.
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

from PyQt5 import QtCore, QtGui
import configparser
import os
from pathlib import Path
from enum import Enum


def constructAbsPath(fileName: str) -> str:
    """
    Constructs absolute path to file with given fileName.
    :param fileName str
    :rtype str
    """
    # get absolute current path
    file_path = os.path.dirname(os.path.abspath(__file__))
    # go to parent directory and add local path
    absPath = Path(file_path).parent.joinpath(fileName)
    return str(absPath)


class LanguageStrings:
    """
    Class for reading/storing all translated information from language file
    """

    defaultLanguageFile = 'configs/de.txt'

    def __init__(self, fileName: str):

        # create parser and read file
        parser = configparser.ConfigParser()
        languageFile = constructAbsPath(fileName)
        if not os.path.isfile(languageFile):
            languageFile = constructAbsPath(LanguageStrings.defaultLanguageFile)
        parser.read(languageFile)

        widget = 'Widgets'
        self.windowTitle_Text = parser[widget]['windowTitle']
        self.chooseStation_Text = parser[widget]['chooseStation']
        self.departure_Text = parser[widget]['departure']
        self.arrival_Text = parser[widget]['arrival']
        self.earlier_Text = parser[widget]['earlier']
        self.later_Text = parser[widget]['later']
        self.now_Text = parser[widget]['now']
        self.request_Text = parser[widget]['request']
        self.refresh_Text = parser[widget]['refresh']
        self.next_Text = parser[widget]['next']
        self.previous_Text = parser[widget]['previous']
        self.ICE_Text = parser[widget]['ICE']
        self.IC_Text = parser[widget]['IC']
        self.other_Text = parser[widget]['other']
        self.showMap_Text = parser[widget]['showMap']
        self.width_Text = parser[widget]['width']
        self.height_Text = parser[widget]['height']
        self.hours_Text = parser[widget]['hours']

        self.from_Text = parser[widget]['from']
        self.to_Text = parser[widget]['to']
        self.track_Text = parser[widget]['track']
        self.time_Text = parser[widget]['time']
        self.name_Text = parser[widget]['name']
        self.stop_Text = parser[widget]['stop']

        menu = 'Menu'
        self.colour_Text = parser[menu]['colour']
        self.application_Text = parser[menu]['application']
        self.quit_Text = parser[menu]['quit']
        self.change_Path_Colour_Text = parser[menu]['change_path']
        self.change_Marker_Colour_Text = parser[menu]['change_marker']
        self.select_Path_Colour_Text = parser[menu]['select_path']
        self.select_Marker_Colour_Text = parser[menu]['select_marker']

        labels = 'Labels'

        self.route_Text = parser[labels]['route']
        self.on_Text = parser[labels]['on']
        self.off_Text = parser[labels]['off']
        self.for_Text = parser[labels]['for']
        self.errorMsg = parser[labels]['errorMsg']


class MapType(Enum):
    """
    Enum type for MapType.
    """
    streets_v10 = 1
    outdoors_v10 = 2
    light_v9 = 3
    dark_v9 = 4
    satellite_v9 = 5
    satellite_streets_v10 = 6
    navigation_preview_day_v4 = 7
    navigation_preview_night_v4 = 8
    navigation_guidance_day_v4 = 9
    navigation_guidance_night_v4 = 10


class RequestSettings:
    """
    Class that encapsulates Request-settings.
    Holds Marker size/color, Path size/color and the height/width
    of the Map that will be requested.
    Holds default values and a minimum for map size.
    Holds the offset used when requesting later/earlier.
    """

    # noinspection SpellCheckingInspection
    def __init__(self, keyFile: str, fileName: str):
        """
        Construct RequestSettings object, that holds all
        possible settings. Read these from given file.
        :type fileName str

        """

        # create parser and read file
        parser = configparser.ConfigParser()
        parser.read(constructAbsPath(keyFile))

        # read keys
        keys = 'Keys'
        try:
            self.DBKey = parser[keys]['DBKey']
            self.MapBoxKey = parser[keys]['GoogleMapsKey']
        except KeyError:
            self.DBKey = None
            self.MapBoxKey = None
        try:
            self.TelegramBotToken = parser[keys]['TelegramToken']
        except KeyError:
            self.TelegramBotToken = None

        parser = configparser.ConfigParser()
        parser.read(constructAbsPath(fileName))

        default = 'Default'
        # read language
        self.LANGUAGE = parser[default]['language']
        languageFileName = 'configs/'+self.LANGUAGE+'.txt'
        # construct langaguageStrings object
        self.LanguageStrings = LanguageStrings(languageFileName)

        # read date/timeformat
        self.dateFormat = parser[default]['dateFormat']
        self.timeFormat = parser[default]['timeFormat']

        # read mapType used
        try:
            self.MAPTYPE = MapType[parser[default]['MapType']].value
        # forced default value
        except KeyError:
            self.MAPTYPE = 1

        # read default color values and sizes
        self.PATH_COLOR = QtGui.QColor(parser[default]['PathColor'])
        self.PATH_SIZE = parser[default]['PathSize']
        self.PATH_OPACITY = parser[default]['PathOpacity']
        self.MARKER_COLOR = QtGui.QColor(parser[default]['MarkerColor'])
        self.MARKER_SIZE = parser[default]['MarkerSize']
        self.MARKER_COLOR_SPECIAL = QtGui.QColor(parser[default]['MarkerColorSpecial'])
        self.MARKER_SIZE_SPECIAL = parser[default]['MarkerSizeSpecial']

        # read default offset and min/max offset
        self.defaultOffSet = int(parser[default]['defaultOffSet'])
        self.offSet = self.defaultOffSet

        # read default and min/max MapSize
        self.defaultSize = int(parser[default]['defaultSize'])
        self.height = self.defaultSize
        self.width = self.defaultSize
        self.minSize = int(parser[default]['minSize'])
        self.maxSize = int(parser[default]['maxSize'])

        # string constants for toStringMethods
        self.departureString = ' (' + self.LanguageStrings.departure_Text + ') '
        self.arrivalString = ' (' + self.LanguageStrings.arrival_Text + ') '
        self.detailsBaseString = self.LanguageStrings.route_Text + ' ' + self.LanguageStrings.off_Text + ' '
        self.generalBaseString = self.LanguageStrings.windowTitle_Text + ' ' + self.LanguageStrings.for_Text + ' '
        self.datePrefix = ' ' + self.LanguageStrings.on_Text + ' '

    def getOffSet(self) -> int:
        """
        Returns the offset to use in seconds.
        :rtype int
        """

        return self.getRealOffSet() * 3600

    def getRealOffSet(self)-> int:
        """
        Returns the offset to use in hours.
        """

        return self.offSet

    def setMarkerColor(self, col: QtGui.QColor):
        """
        Set MarkerColor to given color.
        :type col QtGui.QColor
        """

        self.MARKER_COLOR = col

    def setPathColor(self, col: QtGui.QColor):
        """
        Set PathColor to given color.
        :type col QtGui.QColor
        """

        self.PATH_COLOR = col

    def setHeight(self, h: int):
        """
        Sets height to given value.
        :type h int
        """

        # prevent to small/large size
        if self.minSize <= h <= self.maxSize:
            self.height = h

    def setWidth(self, w: int):
        """
        Sets width to given value.
        :type w int
        """

        # prevent to small/large size
        if self.minSize <= w <= self.maxSize:
            self.width = w

    def setOffSet(self, s: int):
        """
        Sets the offset used when requesting earlier/later to given value.
        :type s int
        """

        if s > 0:
            self.offSet = s


class TrainType(Enum):
    """
    Enum type for TrainType.
    """
    ICE = 1
    TGV = 2
    IC = 3
    EC = 4
    EN = 5
    Other = 6


class Connection:
    """
    Class for encapsulation of a single train-connection.
    """

    def __init__(self, name: str, typ: str, stopId: int, stopName: str, time: QtCore.QTime, date: QtCore.QDate,
                 direction: str, origin: str, track: str, ref: str, url: str):
        """
        Constructs a new new connection from name,type,stopId,
        stopName,time,date,direction,origin,track and reference link, and request used link
        Initializes empty stop-List and image-Data
        :type name str
        :type typ str
        :type stopId int
        :type stopName str
        :type time QtCore.QTime
        :type date QtCore.Date
        :type direction str
        :type origin str
        :type track str
        :type ref str
        :type url str
        """

        # Name e.g. IC10250,ICE516, etc
        self.name = name
        # type number of enum TrainType
        if typ in {'ICE', 'IC', 'EC', 'EC', 'EN', 'TGV'}:
            self.type = TrainType[typ]
        else:
            self.type = 5
        # id of the station which the connection was requested from
        self.stopId = stopId
        # name of station which the connection was requested from
        self.stopName = stopName
        # time corresponding to requested connection and station
        self.time = time
        # date of the connection
        self.date = date
        # direction of connection
        self.direction = direction
        # origin of the connection
        self.origin = origin
        # track of the connection corresponding to requested station
        self.track = track
        # reference link for more details
        self.ref = ref
        # list of all Stops of this connection
        self.stopList = []
        # construct connection with empty imageData
        self.imageData = QtCore.QByteArray()
        # save mapType corresponding to imageData
        self.mapType = 0
        # set link used to request connection
        self.url = url

    def getCoordinatesWithMarker(self) -> ([], int):
        """
        Calculates list of coordinates of all stops of this connection.
        Also returns the index of the stop which the connection was requested from
        :rtype: ([tuple], int)
        """
        coordinates = []
        markerIndex = -1
        for i in range(len(self.stopList)):
            coordinates.append(self.stopList[i].pos)
            if self.stopList[i].id == self.stopId:
                markerIndex = i
        return coordinates, markerIndex

    def isDeparture(self):

        return not self.direction == ""

    def timeToString(self, settings: RequestSettings) -> str:
        """
        Formats the connection time using Qt.Time method.
        :rtype str
        """

        return self.time.toString(settings.timeFormat)

    def dateToString(self, settings: RequestSettings) -> str:
        """
        Formats the connection date using Qt.Date method.
        :rtype str
        """

        return self.date.toString(settings.dateFormat)

    def toStringDetails(self, settings: RequestSettings) -> str:
        """
        Returns a detailed string representation of the connection
        for use in details label.
        :rtype str
        """

        res = settings.detailsBaseString + self.name + settings.datePrefix + self.dateToString(settings)
        return res

    def toStringGeneral(self, settings: RequestSettings) -> str:
        """
        Returns a general String representation of the connection
        for overview.
        :rtype str
        """

        res = settings.generalBaseString + self.stopName
        if self.origin:
            res += settings.arrivalString
        else:
            res += settings.departureString
        res += settings.datePrefix + self.dateToString(settings)
        return res

    def toString(self, settings: RequestSettings) -> str:
        """
        Returns a string representation of the connection
        :rtype str
        """
        if self.direction:
            return self.name + ' ' + settings.LanguageStrings.to_Text + '' + self.direction + ', ' + \
                   self.timeToString(settings) + ', ' + settings.LanguageStrings.track_Text + '' + self.track
        elif self.origin:
            return self.name + ' ' + settings.LanguageStrings.from_Text + ' ' + self.origin + ', ' +\
                   self.timeToString(settings) + ', ' + settings.LanguageStrings.track_Text + '' + self.track


class Stop:
    """
    Class for representing a single stop of a train-connection.
    """

    def __init__(self, name: str, identifier: int, arrTime: QtCore.QTime, arrDate: QtCore.QDate, depTime: QtCore.QTime,
                 depDate: QtCore.QDate, track: str, lon: float, lat: float):
        """
        Constructs stop of name,id, arrivalTime, arrivalDate,
        departureTime, departureDate, Track, longitude, latitude.
        :type name str
        :type identifier int
        :type arrTime QtCore.QTime
        :type arrDate QtCore.QDate
        :type depTime QtCore.QTime
        :type depDate QtCore.QDate
        :type track str
        :type lon float
        :type lat float

        """

        # name of the stop-station
        self.name = name
        # id of the stop-station
        self.id = identifier
        # arrival and departure Time and Date
        self.arrTime = arrTime
        self.arrDate = arrDate
        self.depTime = depTime
        self.depDate = depDate
        # Track from which the connection starts
        self.track = track
        # position of the stop
        self.pos = (lon, lat)

    def arrTimeToString(self, settings: RequestSettings) -> str:
        """
        Formats the stops arrival time using Qt.Time methods
        :rtype str
        """

        return self.arrTime.toString(settings.timeFormat)

    def depTimeToString(self, settings: RequestSettings) -> str:
        """
        Formats the stops departure time using Qt.Time method.
        :rtype str
        """

        return self.depTime.toString(settings.timeFormat)

    def toString(self, settings: RequestSettings) -> str:
        """
        String representation of Stop
        :rtype str
        :
        """

        timeString = self.depTimeToString(settings)
        if not timeString:
            timeString = self.arrTimeToString(settings)
        if self.track:
            track = ', ' + settings.LanguageStrings.track_Text + ' ' + self.track
        else:
            track = ''
        return self.name + ', ' + timeString + track


class ConnectionsList:
    """
    Class for encapsulation of a list of connections.
    Holds a list of lists of connections where each list of connections
    represents one page.
    Holds the index of the displayed page and a tuple (i,j)
    so that details of connection j from page i are  displayed.
    """

    def __init__(self):
        """
        Constructs a connectionList.
        Initialize list empty.
        Set indices to -1.
        """

        self.connectionPages = []
        # thus indices -1
        self.displayedIndex = -1
        self.displayedDetailedIndex = (-1, -1)

    def getSingleConnection(self, pageIndex: int, conIndexOnPage: int) -> Connection:
        """
        Returns the conIndexOnPage'th connection on page PageIndex.
        :type pageIndex int
        :type conIndexOnPage int
        :rtype Connection
        """

        return self.connectionPages[pageIndex][conIndexOnPage]

    def getStop(self, pageIndex: int, conIndexOnPage: int, i: int) -> Stop:
        """
        Returns the i-th stop of connection specified by 2 given indices.
        :type pageIndex int
        :type conIndexOnPage int
        :type i int
        :rtype Stop
        """

        return self.getSingleConnection(pageIndex, conIndexOnPage).stopList[i]

    def getConnectionPage(self, pageIndex: int) -> [Connection]:
        """
        Returns the pageIndex'th list of connection (page).
        :type pageIndex int
        :rtype [Connection]
        """

        return self.connectionPages[pageIndex]

    def getPageCount(self) -> int:
        """
        Returns the amount of pages.
        :rtype int
        """

        return len(self.connectionPages)

    def appendPage(self, connections: [Connection]):
        """
        Appends a list of connections to the end of connectionPages (new Page).
        :type connections [Connection]
        """

        self.connectionPages.append(connections)

    def getDetailsIndices(self) -> (int, int):
        """
        Returns the index of the connection and the index of the page,
        which this connection is on, whose details are currently displayed.
        :rtype (int,int)
        """

        return self.displayedDetailedIndex

    def getDisplayedIndex(self) -> int:
        """
        Returns the index of the page that is currently displayed.
        :rtype int
        """

        return self.displayedIndex

    def setDisplayedIndex(self, val: int):
        """
        Sets the index of the page that is currently displayed to given value.
        :type val int
        """

        self.displayedIndex = val

    def setDisplayedDetailedIndex(self, pageIndex: int, row: int):
        """
        Sets index of the connection whose details are currently displayed to row.
        The connection occurs on page pageIndex in connectionPages.
        :type pageIndex int
        :type row int
        """

        self.displayedDetailedIndex = (pageIndex, row)


class Filter:
    """
    Class for type-based filtering of connections.
    All type-flags that are set True on construction
    are types that should be included after filtering.
    """

    def __init__(self, ICE: bool = False, IC: bool = False, other: bool = False):
        """
        Constructs a filter with the given bool flags
        ICE,IC,other.
        Parameters should be True if the type should be
        included after filtering, false otherwise.
        :type ICE bool
        :type IC bool
        :type other bool
        """

        self.ICE = ICE
        self.IC = IC
        self.other = other

    @staticmethod
    def filterICE(con: Connection) -> bool:
        """
        Returns true if the connection con is of type ICE.
        :type con Connection
        :rtype bool
        """

        return con.type == TrainType.ICE or TrainType.ICE.name in con.name

    @staticmethod
    def filterIC(con: Connection) -> bool:
        """
        Returns true if the connection con is of type IC.
        :type con Connection
        :rtype bool
        """

        # be sure to exclude ICE here
        return (con.type == TrainType.IC or TrainType.IC.name in con.name) and not Filter.filterICE(con)

    @staticmethod
    def filterEC(con: Connection) -> bool:
        """
        Returns true if the connection con is of type EC.
        :type con Connection
        :rtype bool
        """

        return con.type == TrainType.EC or TrainType.EC.name in con.name

    @staticmethod
    def filterTGV(con: Connection) -> bool:
        """
        Returns true if the connection con is of type TGV.
        :type con Connection
        :rtype bool
        """

        return con.type == TrainType.TGV or TrainType.TGV.name in con.name

    @staticmethod
    def filterOther(con: Connection) -> bool:
        """
        Returns true if the connection is not of type filtered before.
        :type con Connection
        :rtype bool
        """

        # connection has train type other if it does not have an above stated train type
        return not (Filter.filterICE(con) or Filter.filterIC(con) or Filter.filterEC(con) or Filter.filterTGV(con))

    def filter(self, connections: [Connection]) -> [int]:
        """
        Filters a list of connections by filtering each connection.
        Only filters on type if type flag was set.
        Groups ICE/TGV to ICE, EC/IC to IC.
        Returns list of original indices of all connections that passed filter.
        :type connections [Connection]
        :rtype [int]
        """

        res = []
        # iterate over all connections in list
        for i in range(len(connections)):
            # initial train is not selected
            selected = False
            # for each selected filter type check if connection has this type
            if self.ICE:
                selected = Filter.filterICE(connections[i]) or Filter.filterTGV(connections[i])
            if self.IC:
                selected = selected or Filter.filterIC(connections[i]) or Filter.filterEC(connections[i])
            if self.other:
                selected = selected or Filter.filterOther(connections[i])
            # connection passes filter
            if selected:
                # add index of connection to list
                res.append(i)
        # return list of indices
        return res

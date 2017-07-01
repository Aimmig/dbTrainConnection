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


class ConnectionsSettings:
    """ 
    Class that holds all relevant constant and fix options
    for formatting and converting connection to String.
    Holds base strings for string representation
    (general and details) of a connection.
    Holds time and date formatting strings.
    """

    # format date as dd.M.yy
    dateFormat = "dd.M.yy"
    # format time as hh:mm
    timeFormat = "hh:mm"
    # string constants for toStringMethods
    departureString = " (Abfahrt) "
    arrivalString = " (Ankunft) "
    detailsBaseString = "Zugverlauf von "
    generalBaseString = "Fahrplantabelle für "
    datePrefix = " am "


class Connection:
    """
    Class for encapsulation of a single train-connection.
    """

    def __init__(self, name: str, typ: str, stopId: int, stopName: str, time: QtCore.QTime, date: QtCore.QDate,
                 direction: str, origin: str, track: str, ref: str):
        """
        Constructs a new new connection from name,type,stopId,
        stopName,time,date,direction,origin,track and reference link.
        Initializes empty stop-List and image-Data.
        """

        # Name e.g. IC10250,ICE516, etc
        self.name = name
        # Typ: IC,ICE, EC,..
        self.type = typ
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

    def timeToString(self):
        """
        Formats the connection time using Qt.Time method
        with format specified in ConnectionsSettings.
        """

        return self.time.toString(ConnectionsSettings.timeFormat)

    def dateToString(self):
        """
        Formats the connection date using Qt.Date method
        with format specified in ConnectionsSettings.
        """

        return self.date.toString(ConnectionsSettings.dateFormat)

    def toStringDetails(self):
        """
        Returns a detailed string representation of the connection
        for use in details label.
        """

        res = ConnectionsSettings.detailsBaseString + self.name + ConnectionsSettings.datePrefix + self.dateToString()
        return res

    def toStringGeneral(self):
        """
        Returns a general String representation of the connection
        for overview.
        """

        res = ConnectionsSettings.generalBaseString + self.stopName
        if self.origin:
            res += ConnectionsSettings.arrivalString
        else:
            res += ConnectionsSettings.departureString
        res += ConnectionsSettings.datePrefix + self.dateToString()
        return res


class Stop:
    """
    Class for representing a single stop of a train-connection.
    """

    def __init__(self, name: str, identifier: int, arrTime: QtCore.QTime, arrDate: QtCore.QDate, depTime: QtCore.QTime,
                 depDate: QtCore.QDate, track: str, lon: float, lat: float):
        """
        Constructs stop of name,id, arrivalTime, arrivalDate,
        departureTime, departureDate, Track, longitude, latitude.
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
        self.pos = Coordinate(lon, lat)

    def arrTimeToString(self):
        """
        Formats the stops arrival time using Qt.Time method
        with format specified in ConnectionsSettings.
        """

        return self.arrTime.toString(ConnectionsSettings.timeFormat)

    def depTimeToString(self):
        """
        Formats the stops departure time using Qt.Time method
        with format specified in ConnectionsSettings.
        """

        return self.depTime.toString(ConnectionsSettings.timeFormat)


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

        # no information at construction
        self.connectionPages = []
        # thus indices -1
        self.displayedIndex = -1
        self.displayedDetailedIndex = (-1, -1)

    def getSingleConnection(self, pageIndex: int, conIndexOnPage: int):
        """
        Returns the conIndexOnPage'th connection on page PageIndex.
        """

        return self.connectionPages[pageIndex][conIndexOnPage]

    def getStop(self, pageIndex: int, conIndexOnPage: int, i: int):
        """
        Returns the i-th stop of connection specified by 2 given indices.
        """

        return self.getSingleConnection(pageIndex, conIndexOnPage).stopList[i]

    def getConnectionPage(self, pageIndex: int):
        """
        Returns the pageIndex'th list of connection (page).
        """

        return self.connectionPages[pageIndex]

    def getPageCount(self):
        """
        Returns the amount of pages.
        """

        return len(self.connectionPages)

    def appendPage(self, connections):
        """
        Appends a list of connections to the end of connectionPages (new Page).
        """

        self.connectionPages.append(connections)

    def getDetailsIndices(self):
        """
        Returns the index of the connection and the index of the page,
        which this connection is on, whos details are currently displayed.
        """

        return self.displayedDetailedIndex

    def getDisplayedIndex(self):
        """
        Returns the index of the page that is currently displayed.
        """

        return self.displayedIndex

    def setDisplayedIndex(self, val: int):
        """
        Sets the index of the page that is currently displayed to given value.
        """

        self.displayedIndex = val

    def setDisplayedDetailedIndex(self, pageIndex: int, row: int):
        """
        Sets index of the connection whos details are currently displayed to row.
        The connection occurs on page pageIndex in connectionPages.
        """

        self.displayedDetailedIndex = (pageIndex, row)


class Coordinate:
    """
    Class for representing a geographical coordinate.
    """

    def __init__(self, lon: float, lat: float):
        """
        Constructs Coordinate from longitude and longitude.
        """

        self.lon = lon
        self.lat = lat


class Filter:
    """
    Class for type-based filtering of connections.
    All type-flags that are set True on construction
    are types that should be included after filtering.
    """

    def __init__(self, ICE: bool, IC: bool, other: bool):
        """
        Constructs a filter with the given bool flags
        ICE,IC,other.
        Parameters should be True if the type should be
        included after filtering, false otherwise.        
        """

        self.ICE = ICE
        self.IC = IC
        self.other = other

    @staticmethod
    def filterICE(con: Connection):
        """
        Returns true if the connection con is of type ICE.
        """

        return con.type == "ICE" or "ICE" in con.name

    @staticmethod
    def filterIC(con: Connection):
        """
        Returns true if the connection con is of type IC.
        """

        # be sure to exclude ICE here
        return con.type == ("IC" or "IC" in con.name) and not Filter.filterICE(con)

    @staticmethod
    def filterEC(con: Connection):
        """
        Returns true if the connection con is of type EC.
        """

        return con.type == "EC" or "EC" in con.name

    @staticmethod
    def filterTGV(con: Connection):
        """
        Returns true if the connection con is of type TGV.
        """

        return con.type == "TGV" or "TGV" in con.name

    @staticmethod
    def filterOther(con: Connection):
        """
        Returns true if the connection is not of type filtered before.
        """

        # connection has train type other if it does not have an above stated train type
        return not (Filter.filterICE(con) or Filter.filterIC(con) or Filter.filterEC(con) or Filter.filterTGV(con))

    def filter(self, connections: ConnectionsList):
        """
        Filters a list of connections by filtering each connection.
        Only filters on type if type flag was set.
        Groups ICE/TGV to ICE, EC/IC to IC.
        Returns list of original indices of all connections that passed filter.
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


class RequestSettings:
    """
    Class that encapsulates Request-settings.
    Holds Marker size/color, Path size/color and the height/width
    of the Map that will be requested.
    Holds default values and a minimum for map size.
    Holds the offset used when requesting later/earlier.
    """

    # static settings that can not be changed (at the moment)
    MARKER_SIZE = 'small'
    MARKER_SIZE_SPECIAL = 'mid'
    PATH_SIZE = '3'
    MARKER_COLOR_SPECIAL = QtGui.QColor('#aa339988')
    MIN_SIZE = 300

    def __init__(self, defaultSize: int, defaultOffSet: int):
        """
        Construct RequestSettings with given defaultSize of the map
        and the default offset used when requesting earlier/later.
        """

        self.PATH_COLOR = QtGui.QColor('#ff0000')
        self.MARKER_COLOR = QtGui.QColor('#5555BB')
        self.height = defaultSize
        self.width = defaultSize
        self.offSet = defaultOffSet

    def formatPathColor(self):
        """
        Returns string representation of the PathColor that can be used in URL.
        """

        return self.PATH_COLOR.name().replace('#', '0x')

    def formatColor(self):
        """
        Returns string representation of the MarkerColor that can be used in URL.
        """

        return self.MARKER_COLOR.name().replace('#', '0x')

    @staticmethod
    def formatSpecialColor():
        """
        Returns string representation of the MarkerColorSpecial that can be used in URL.
        """

        return RequestSettings.MARKER_COLOR_SPECIAL.name().replace('#', '0x')

    def setMarkerColor(self, col: QtGui.QColor):
        """
        Set MarkerColor to given color.
        """

        self.MARKER_COLOR = col

    def setPathColor(self, col: QtGui.QColor):
        """
        Set PathColor to given color.   
        """

        self.PATH_COLOR = col

    def setHeight(self, h: int):
        """
        Sets height to given value.
        If below minimum use minimum.
        """

        # prevent to small size
        if h >= RequestSettings.MIN_SIZE:
            self.height = h
        else:
            self.height = RequestSettings.MIN_SIZE

    def setWidth(self, w: int):
        """
        Sets width to given value.
        If below minimum use minimum.
        """

        # prevent to small size
        if w >= RequestSettings.MIN_SIZE:
            self.width = w
        else:
            self.width = RequestSettings.MIN_SIZE

    def setOffSet(self, s: int):
        """
        Sets the offset used when requesting earlier/later to given value.
        """

        # do not set invalid offsets
        if s <= 0:
            return
        self.offSet = s

#    -----------------------------------------------------------------------
#    This program requests connections and corresponding details from the
#    API of Deutsche Bahn and presents them in an user interface
#    This file encapsulates the parsing of the requested xml string into 
#    instances of the data structures.
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

import xml.etree.ElementTree as ET
from PyQt5 import QtCore
from Structs import Stop, Connection


class XMLParser:
    """
    Static class for parsing the requested information out of
    the XML-String and convert it to objects.
    """

    # constants for parsing xml-Document
    Id = 'id'
    NAME = 'name'
    TYPE = 'type'
    StopId = 'stopid'
    Stop = 'stop'
    TIME = 'time'
    DATE = 'date'
    ORIGIN = 'origin'
    DIRECTION = 'direction'
    TRACK = 'track'
    REF = 'ref'
    ArrTime = 'arrTime'
    ArrDate = 'arrDate'
    DepTime = 'depTime'
    DepDate = 'depDate'
    LON = 'lon'
    LAT = 'lat'
    STOPS = 'Stops'
    DATE_FORMAT = 'yyyy-MM-dd'
    TIME_FORMAT = 'hh:mm'

    @staticmethod
    def getStationsFromXMLString(xmlString: str)->([int], [str]):
        """
        Parses the xmlString and returns a list of all stop names
        and a list of all corresponding id's of these stops.
        :type xmlString: str
        :rtype ([int],[str])
        """

        root = ET.fromstring(xmlString)
        # write id and names to temporary variable
        stations = []
        station_ids = []
        # iterate over all children and add attributes to lists
        for child in root:
            station_ids.append(int(child.attrib[XMLParser.Id]))
            stations.append(child.attrib[XMLParser.NAME])
        return stations, station_ids

    @staticmethod
    def getConnectionsFromXMLString(xmlString: str, isDeparture: bool)-> [Connection]:
        """
        Parses xmlString and returns list of all connections
        contained in the string.
        Takes a boolean flag isDeparture to ensure departure/arrival.
        Returns empty string on parsing error.
        :type xmlString str
        :type isDeparture bool
        :rtype [Connection]
        """

        try:
            # load xmlString in element tree
            root = ET.fromstring(xmlString)
            connections = []
            # iterate over all connections
            for con in root:
                # connection name is mandatory
                name = con.attrib[XMLParser.NAME]
                # check if type exist
                if XMLParser.TYPE in con.attrib:
                    typ = con.attrib[XMLParser.TYPE]
                # avoid spelling mistake in xml
                else:
                    typ = ''
                # stop, id and time, date are mandatory
                stopId = int(con.attrib[XMLParser.StopId])
                stopName = con.attrib[XMLParser.Stop]
                # convert time and date string to Qt Objects
                timeString = con.attrib[XMLParser.TIME]
                time = QtCore.QTime.fromString(timeString, XMLParser.TIME_FORMAT)
                dateString = con.attrib[XMLParser.DATE]
                date = QtCore.QDate.fromString(dateString, XMLParser.DATE_FORMAT)
                # read direction if is departure and departure exists
                if isDeparture and XMLParser.DIRECTION in con.attrib:
                    # set direction
                    direction = con.attrib[XMLParser.DIRECTION]
                    origin = ''
                # read origin if is not departure and origin exits
                elif not isDeparture and XMLParser.ORIGIN in con.attrib:
                    # set origin
                    origin = con.attrib[XMLParser.ORIGIN]
                    direction = ''
                # invalid case might happen
                else:
                    # set both attributes to ""
                    origin = ''
                    direction = ''
                # track might not be set in xml
                if XMLParser.TRACK in con.attrib:
                    track = con.attrib[XMLParser.TRACK]
                else:
                    track = ''
                # read reference link
                ref = ''
                for details in con:
                    if XMLParser.REF in details.attrib:
                        ref = details.attrib[XMLParser.REF]
                # add connection with these information to local list of connections
                connections.append(Connection(name, typ, stopId, stopName, time, date, direction, origin, track, ref))
            return connections
        except ET.ParseError:
            return []

    @staticmethod
    def getStopListFromXMLString(xmlString: str) -> [Stop]:
        """
        Parses xmlString and returns list of all stops of a connection
        contained in the string.
        Returns empty string on parsing error.
        :type xmlString: str
        :rtype [Stop]
        """

        try:
            # load xmlString to element Tree
            root = ET.fromstring(xmlString)
            stopList = []
            # iterate over all children c
            for c in root:
                # only use Stop children of c
                if c.tag == XMLParser.STOPS:
                    # iterate over all single Stops
                    for child in c:
                        # name and id of the station are mandatory
                        name = child.attrib[XMLParser.NAME]
                        identifier = int(child.attrib[XMLParser.Id])
                        # check if arrival time exists
                        if XMLParser.ArrTime in child.attrib:
                            # read arrival time
                            arrTimeString = child.attrib[XMLParser.ArrTime]
                            # convert arrival time to QTime
                            arrTime = QtCore.QTime.fromString(arrTimeString, XMLParser.TIME_FORMAT)
                        else:
                            arrTime = QtCore.QTime()
                        # check if arrival date exists
                        if XMLParser.ArrDate in child.attrib:
                            # read arrival date
                            arrDateString = child.attrib[XMLParser.ArrDate]
                            # convert arrival date to QDate
                            arrDate = QtCore.QDate.fromString(arrDateString, XMLParser.DATE_FORMAT)
                        else:
                            arrDate = QtCore.QDate()
                        # check if departure time exists
                        if XMLParser.DepTime in child.attrib:
                            # read departure Time
                            depTimeString = child.attrib[XMLParser.DepTime]
                            # convert departure time to QTime
                            depTime = QtCore.QTime.fromString(depTimeString, XMLParser.TIME_FORMAT)
                        else:
                            depTime = QtCore.QTime()
                        # check if departure date exists
                        if XMLParser.DepDate in child.attrib:
                            # read departure date
                            depDateString = child.attrib[XMLParser.DepDate]
                            # convert departure date to QDate object
                            depDate = QtCore.QDate.fromString(depDateString, XMLParser.DATE_FORMAT)
                        else:
                            depDate = QtCore.QDate()
                        # track might not be set
                        if XMLParser.TRACK in child.attrib:
                            track = child.attrib[XMLParser.TRACK]
                        else:
                            track = ''
                        # longitude, latitude are mandatory
                        lon = float(child.attrib[XMLParser.LON])
                        lat = float(child.attrib[XMLParser.LAT])
                        # create stop with all these information
                        stop = Stop(name, identifier, arrTime, arrDate, depTime, depDate, track, lon, lat)
                        # add it to local list
                        stopList.append(stop)
            # return list of all stops
            return stopList
        except ET.ParseError:
            return []

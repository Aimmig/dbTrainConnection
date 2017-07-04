# -*- coding: utf-8 -*-
#    -----------------------------------------------------------------------
#    This program requests connections and corresponding details from the
#    API of Deutsche Bahn and presents them in an user interface.
#    This file encapsulates the main gui, handles the gui navigation and
#    defines logic to display the information.
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

from PyQt5 import QtCore, QtGui, QtWidgets
from Widgets import QConnectionTable, QDetailsTable, QMapWidget
from Request import Request
from Structs import Connection, ConnectionsList, Stop, Filter, Coordinate
from SettingsWidget import SettingsWidget
from XMLParser import XMLParser as parser
import sys
import urllib.error as err


class FormWidget(QtWidgets.QWidget):
    """
    Main Gui consist of three parts.
    Part 1 for user input,
    part 2 for displaying general information for connections
    part 3 for displaying detailed information for one connection.
    Additionally holds important global variables.
    """

    def __init__(self):
        """
        Constructor initializes main gui.
        Initializes settings- and mapWidget.
        """

        # super constructor
        # noinspection PyArgumentList
        super(FormWidget, self).__init__()

        # create MenuBar with self as parent
        self.myQMenuBar = QtWidgets.QMenuBar(self)

        # create MenuBars
        self.initializeMenuBar()

        # set Window Title
        self.setWindowTitle('Fahrplananzeige')
        # set default error Message
        self.errorMsg = 'Keine Information  vorhanden'
        # create empty list for station Ids
        self.stationId = []
        # initialize ConnectionList
        self.conList = ConnectionsList()
        # set filter to active
        self.filterActive = True
        # initialize Widget for map
        self.mapWidget = QMapWidget()
        # initialize SettingsWidget
        self.settingsWidget = SettingsWidget()

        # create HorizontalBoxLayout as overall Widget layout
        layout = QtWidgets.QHBoxLayout()

        # initialize three main layout parts
        box1 = self.initializeUserInputLayout()
        box2 = self.initializeConnectionTableLayout()
        box3 = self.initializeDetailsTableLayout()

        # add all layouts to form-Layout
        layout.addLayout(box1)
        layout.addLayout(box2)
        layout.addLayout(box3)

        # set formLayout
        self.setLayout(layout)
        # create empty Filter
        self.typeFilter = Filter()

    # noinspection PyUnresolvedReferences
    def initializeMenuBar(self):
        """
        Initializes QMenuBar.
        Adds action for choosing path and marker color.
        Adds action for showing the settingsWidget.
        """

        # create Menu for changing settings
        settingsMenu = self.myQMenuBar.addMenu('Einstellung')
        # create Action for changing settings
        settingsAction = QtWidgets.QAction('Ändern', self)
        # connect Action with method
        settingsAction.triggered.connect(self.showSettingsWidget)
        # add Action to Menu
        settingsMenu.addAction(settingsAction)

        # create Menu for changing Colors
        colorMenu = self.myQMenuBar.addMenu('Farben')
        # create Action for changing Path color
        colorPathAction = QtWidgets.QAction('Pfad-Farbe ändern', self)
        # connect Action with method
        colorPathAction.triggered.connect(self.changePathColor)
        # add Action to Menu
        colorMenu.addAction(colorPathAction)
        # create Action for changing Marker Color
        colorMarkerAction = QtWidgets.QAction('Marker-Farbe ändern', self)
        # connect Action with method
        colorMarkerAction.triggered.connect(self.changeMarkerColor)
        # add Action to Menu
        colorMenu.addAction(colorMarkerAction)

        # create Menu for application
        exitMenu = self.myQMenuBar.addMenu('Anwendung')
        # create Action for closing application
        exitAction = QtWidgets.QAction('Beenden', self)
        # connect Action with method
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        # add Action to Menu
        exitMenu.addAction(exitAction)

    # noinspection PyUnresolvedReferences,PyAttributeOutsideInit,PyArgumentList
    def initializeUserInputLayout(self) -> QtWidgets.QVBoxLayout:
        """
        Initializes first part of the gui.
        Initializes LineEdit, ComboBox,
        Date- and Time-Chooser and Radio-Buttons for filtering.
        Additionally initializes the departure/arrival Radio-Button
        and the request buttons.
        """

        # create VerticalBoxLayouts
        layout = QtWidgets.QVBoxLayout()

        # input field for user input
        self.inp = QtWidgets.QLineEdit()
        # button for getting stations
        self.chooseStation = QtWidgets.QPushButton('Bahnhof wählen')
        self.chooseStation.clicked.connect(self.getStations)

        # group input and button in input_layout1
        input1_layout = QtWidgets.QHBoxLayout()
        input1_layout.addWidget(self.inp)
        input1_layout.addWidget(self.chooseStation)

        # comboBox for all Stations
        self.railStations = QtWidgets.QComboBox()
        # time chooser for selecting time
        self.time_chooser = QtWidgets.QTimeEdit()

        # group combo box and time picker in input_layout2
        input2_layout = QtWidgets.QHBoxLayout()
        input2_layout.addWidget(self.railStations)
        input2_layout.addWidget(self.time_chooser)

        # calendar for selecting date
        self.date_chooser = QtWidgets.QCalendarWidget()

        # buttons for getting all connections with System Time
        self.request_now = QtWidgets.QPushButton('Jetzt')
        self.request_now.clicked.connect(self.getConnectionsNow)
        # button for getting connections with chosen Time
        self.request_chosenTime = QtWidgets.QPushButton('Anfragen')
        self.request_chosenTime.clicked.connect(self.getConnectionsWithTime)

        # group time_chooser and request in request_layout
        request_layout = QtWidgets.QHBoxLayout()
        request_layout.addWidget(self.request_now)
        request_layout.addWidget(self.request_chosenTime)

        # create RadioButtons for departure/arrival selection
        self.depart = QtWidgets.QRadioButton('Abfahrten')
        self.arriv = QtWidgets.QRadioButton('Ankünfte')
        # group RadioButtons
        radioButton_layout = QtWidgets.QHBoxLayout()
        radioButton_layout.addWidget(self.depart)
        radioButton_layout.addWidget(self.arriv)
        # set departure to default checked
        self.depart.setCheckable(True)
        self.arriv.setCheckable(True)
        self.depart.setChecked(True)

        # create Horizontal Layout for filtering
        filterLayout = QtWidgets.QHBoxLayout()
        # create CheckBoxes for activating Filtering
        self.checkFilter = QtWidgets.QCheckBox(' Filter ')
        # create CheckBoxes for choosing filters
        self.checkICE = QtWidgets.QCheckBox(' ICE/TGV ')
        self.checkIC = QtWidgets.QCheckBox(' IC/EC ')
        self.checkOther = QtWidgets.QCheckBox(' other ')
        # add checkboxes to filterLayout
        filterLayout.addWidget(self.checkFilter)
        filterLayout.addWidget(self.checkICE)
        filterLayout.addWidget(self.checkIC)
        filterLayout.addWidget(self.checkOther)

        # create Layout for activating map
        mapLayout = QtWidgets.QHBoxLayout()
        # create CheckBox for en/disabling map
        self.mapActive = QtWidgets.QCheckBox(' Karte anzeigen ')
        # add checkbox to layout
        mapLayout.addWidget(self.mapActive)

        # create buttons for getting connections earlier/later and group them
        requestEarlierLater_layout = QtWidgets.QHBoxLayout()
        self.earlier = QtWidgets.QPushButton('Früher')
        self.later = QtWidgets.QPushButton('Später')
        self.later.clicked.connect(self.getConnectionsLater)
        self.earlier.clicked.connect(self.getConnectionsEarlier)
        requestEarlierLater_layout.addWidget(self.earlier)
        requestEarlierLater_layout.addWidget(self.later)

        # add layouts and widgets to layout
        layout.addLayout(input1_layout)
        layout.addLayout(input2_layout)
        layout.addWidget(self.date_chooser)
        layout.addLayout(radioButton_layout)
        layout.addLayout(filterLayout)
        layout.addLayout(mapLayout)
        layout.addLayout(requestEarlierLater_layout)
        layout.addLayout(request_layout)

        return layout

    # noinspection PyUnresolvedReferences,PyAttributeOutsideInit,PyArgumentList
    def initializeConnectionTableLayout(self) -> QtWidgets.QVBoxLayout:
        """
        Initializes part 2 of the gui.
        This includes a label for general information,
        the QConnectionTable and buttons for navigation and
        refreshing.
        """

        # create VerticalBoxLayout
        layout = QtWidgets.QVBoxLayout()

        # label for connectionTable
        self.connection_label = QtWidgets.QLabel('')
        # QTableWidget for displaying connections
        self.connectionTable = QConnectionTable(self)
        # connect connectionTable with function
        self.connectionTable.clicked.connect(self.getDetails)

        # button for navigating
        self.prev = QtWidgets.QPushButton('Vorherige')
        self.prev.clicked.connect(self.showPreviousPage)
        # button for refreshing the page using new filter
        self.reload = QtWidgets.QPushButton('Aktualisieren')
        self.reload.clicked.connect(self.refreshPage)
        # button for navigating
        self.next = QtWidgets.QPushButton('Nächste')
        self.next.clicked.connect(self.showNextPage)

        # layout for navigation
        navigation_layout = QtWidgets.QHBoxLayout()
        # add buttons to navigation layout
        navigation_layout.addWidget(self.prev)
        navigation_layout.addWidget(self.reload)
        navigation_layout.addWidget(self.next)

        # add widgets and navigationLayout to layout
        layout.addWidget(self.connection_label)
        layout.addWidget(self.connectionTable)
        layout.addLayout(navigation_layout)

        return layout

    # noinspection PyUnresolvedReferences,PyAttributeOutsideInit,PyArgumentList
    def initializeDetailsTableLayout(self) -> QtWidgets.QVBoxLayout:
        """
        Initializes part 3 of the gui.
        This includes a label for displaying information for a connection
        and the QDetailsTable.
        """

        # create VerticalBoxLayout
        layout = QtWidgets.QVBoxLayout()

        # label for details of a connection
        self.details_label = QtWidgets.QLabel('')
        # QTableWidget for presenting detailed data of a connection
        self.detailsTable = QDetailsTable(self)
        # connect QTableWidget with function
        self.detailsTable.clicked.connect(self.getConnectionsOnClickInDetails)

        # add label
        layout.addWidget(self.details_label)
        # add QTableWidget
        layout.addWidget(self.detailsTable)
        # return layout with added widgets
        return layout

    def getConnectionsOnClickInDetails(self):
        """
        Called on click in DetailsTable.
        Request (departure) connections for station,time,date from selected row.
        Calls getConnections with the parameters read from this row.
        """

        # get selected Row in connection details
        row = self.detailsTable.currentRow()
        # avoid error if nothing is selected
        if row < 0:
            return
        # get the displayedIndex Information
        (pageIndex, connectionIndexOnPage) = self.conList.getDetailsIndices()
        # select the clicked stop from the displayed Connection (Details)
        s = self.conList.getStop(pageIndex, connectionIndexOnPage, row)
        # default use arrival Date and Time
        date = s.arrDate
        time = s.arrTime
        # if date or time are invalid try using depDate/time
        if not date or not time:
            date = s.depDate
            time = s.depTime
        identifier = s.id
        # request information and display it
        self.getConnections(date, time, identifier, True)

    def clearDetailsTable(self):
        """
        Clears the detailsTable by setting RowCount to 0.
        """

        self.detailsTable.setRowCount(0)

    def getDetails(self):
        """
        Called on click in ConnectionTables.
        Uses reference link of the selected connection to request 
        detailed information (if needed) for this connection.
        Displays this detailed information in DetailsTable.
        """

        # get the selected Index
        index = self.connectionTable.currentRow()
        # avoid error if nothing was selected
        if index < 0:
            return
        # get the connection according to the index
        connection = self.conList.getSingleConnection(self.conList.getDisplayedIndex(), index)
        # if stopList is empty request details information
        if not connection.stopList:
            # get reference link of connection
            urlString = connection.ref
            try:
                # request xml String
                xmlString = Request.getXMLStringConnectionDetails(urlString)
            except err.HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                return
            except err.URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
                return
            stopList = parser.getStopListFromXMLString(xmlString)
            if stopList:
                # set the stopList of the connection to the local list
                connection.stopList = stopList
            else:
                self.clearDetailsTable()
                self.details_label.setText(self.errorMsg)
                return
        coordinates, markerIndex = self.addAllStopsToDetails(connection, index)
        self.RequestAndShowMap(connection, coordinates, markerIndex)

    def addAllStopsToDetails(self, connection: Connection, index: int) -> ([Coordinate], int):
        """
        Adds all Stops of the given Connection to DetailsTable.
        Sets the the displayedDetailedIndex to given index.
        Sets the Details_label text.
        In term calculates a list of Coordinates and the index of the stop for special markerIndex
        and returns this as result.
        :type connection: Connection
        :type index: int
        :rtype ([Coordinate],int)
        """

        markerIndex = -1
        coordinates = []
        # clear detailsTable
        self.clearDetailsTable()
        # for every stop in stopList add it to QTableWidget
        for i in range(len(connection.stopList)):
            self.addStopToDetails(connection.stopList[i])
            coordinates.append(connection.stopList[i].pos)
            if connection.stopList[i].id == connection.stopId:
                markerIndex = i
        # set details_label text to connection information
        self.details_label.setText(connection.toStringDetails())
        self.conList.setDisplayedDetailedIndex(self.conList.getDisplayedIndex(), index)
        return coordinates, markerIndex

    def RequestAndShowMap(self, connection: Connection, coordinates: [Coordinate], markerIndex: int):
        """
        Checks if Map-Data needs to be requested.
        If so request map-Data with coordinates and markerIndex.
        Displays the map-Data.
        :type connection Connection
        :type coordinates [Coordinate]
        :type markerIndex int
        """

        # check if imageData is empty and if map is selected
        if connection.imageData.isEmpty() and self.mapActive.isChecked():
            # request imageData and create QByteArray and set imageData
            # noinspection PyArgumentList
            connection.imageData = QtCore.QByteArray(
                Request.getMapWithLocations(coordinates, markerIndex, self.settingsWidget.settings))
        # display requested map-Data
        if self.mapActive.isChecked():
            self.mapWidget.showMap(connection.imageData, connection.toStringDetails())

    def showPreviousPage(self):
        """
        Display previous page of requested connections.
        Does not have an effect on first page.
        """

        if self.conList.getDisplayedIndex() > 0:
            self.conList.setDisplayedIndex(self.conList.getDisplayedIndex() - 1)
            # remove old elements from QTableWidget
            self.clearConnectionTable()
            # for every connection add connection display it
            self.addConnections(self.conList.getConnectionPage(self.conList.getDisplayedIndex()))
            self.setConnectionLabel()

    def refreshPage(self):
        """
        Refreshes displayed connection page.
        First clears ConnectionTable.
        Applies changed filter to original data
        and displays new results.
        """

        index = self.conList.getDisplayedIndex()
        if index >= 0:
            self.clearConnectionTable()
            self.addConnections(self.conList.getConnectionPage(index))

    def clearConnectionTable(self):
        """
        Clears the ConnectionTable by setting the rowCount to 0.
        """

        self.connectionTable.setRowCount(0)

    def showNextPage(self):
        """
        Displays next page of requested connections.
        Does not have an effect on last page.
        """

        if self.conList.getDisplayedIndex() < self.conList.getPageCount() - 1:
            self.conList.setDisplayedIndex(self.conList.getDisplayedIndex() + 1)
            # remove all elements from QTableWidget
            self.clearConnectionTable()
            # for every connection add connection display it
            self.addConnections(self.conList.getConnectionPage(self.conList.getDisplayedIndex()))
            # resize columns to content
            self.setConnectionLabel()

    def addConnections(self, connections: [Connection]):
        """
        Adds every connection in connections to ConnectionTable.
        Instantiates a filter according to checkbox from userInput.
        If filter is active filters all connection and only displays
        connections that pass the filter.
        """

        self.filterActive = self.checkFilter.isChecked()
        ICE = self.checkICE.isChecked()
        IC = self.checkIC.isChecked()
        Other = self.checkOther.isChecked()
        # minimum one filter type must be selected
        if ICE or IC or Other:
            self.typeFilter = Filter(ICE, IC, Other)
        else:
            self.filterActive = False
        # add all connections to table
        for c in connections:
            self.addConnectionToTable(c)
        # displayed connections shall be filtered
        if self.filterActive:
            # all Indices of original connections that shall be displayed
            displayIndex = self.typeFilter.filter(connections)
            # for each index in the list
            for ind in displayIndex:
                # display corresponding row
                self.connectionTable.setRowHidden(ind, False)
        # select first element
        self.connectionTable.selectRow(0)

    def setConnectionLabel(self):
        """
        Sets the connection label to the string representation of the first
        displayed connection.
        """

        self.connection_label.setText(
            self.conList.getSingleConnection(self.conList.getDisplayedIndex(), 0).toStringGeneral())

    def addConnectionToTable(self, con: Connection):
        """
        Adds the given connection as a new row to ConnectionTable.
        When filter is used the new row is set to hidden default.
        """

        # add new row to QTableWidget
        self.connectionTable.insertRow(self.connectionTable.rowCount())
        # select last row of QTableWidget
        row = self.connectionTable.rowCount() - 1
        # for active filter hide everything on default
        if self.filterActive:
            self.connectionTable.setRowHidden(row, True)
        # add name of connection
        self.connectionTable.setItem(row, QConnectionTable.name_Index, QtWidgets.QTableWidgetItem(con.name))
        # check if direction and origin are valid and add them
        # note that direction (departure) an origin (arrival) are exclusive only one can be set!
        if con.direction:
            self.connectionTable.setItem(row, QConnectionTable.to_Index, QtWidgets.QTableWidgetItem(con.direction))
            self.connectionTable.setItem(row, QConnectionTable.from_Index, QtWidgets.QTableWidgetItem(con.stopName))
        if con.origin:
            self.connectionTable.setItem(row, QConnectionTable.from_Index, QtWidgets.QTableWidgetItem(con.origin))
            self.connectionTable.setItem(row, QConnectionTable.to_Index, QtWidgets.QTableWidgetItem(con.stopName))
        # add time of connection
        self.connectionTable.setItem(row, QConnectionTable.time_Index, QtWidgets.QTableWidgetItem(con.timeToString()))
        # if track is set add track of connection
        if con.track:
            self.connectionTable.setItem(row, QConnectionTable.track_Index, QtWidgets.QTableWidgetItem(con.track))

    def addStopToDetails(self, stop: Stop):
        """
        Adds the given stop as a new row to DetailsTable.
        """

        # insert new row in QTableWidget details
        self.detailsTable.insertRow(self.detailsTable.rowCount())
        # select last row of QTableWidget details
        row = self.detailsTable.rowCount() - 1
        # add stopName
        self.detailsTable.setItem(row, QDetailsTable.stop_Index, QtWidgets.QTableWidgetItem(stop.name))
        # check if times and track are valid and add them
        if stop.arrTime:
            self.detailsTable.setItem(row, QDetailsTable.arr_Index, QtWidgets.QTableWidgetItem(stop.arrTimeToString()))
        if stop.depTime:
            self.detailsTable.setItem(row, QDetailsTable.dep_Index, QtWidgets.QTableWidgetItem(stop.depTimeToString()))
        if stop.track:
            self.detailsTable.setItem(row, QDetailsTable.track_Index, QtWidgets.QTableWidgetItem(stop.track))

    def getStations(self):
        """
        Request all names and corresponding id's for stops that match
        the user input and displays names in corresponding combo-box.
        """

        loc = self.inp.text()
        # check for empty input
        if loc.strip():
            try:
                # create xml-object
                xmlString = Request.getXMLStringStationRequest(loc, self.settingsWidget.settings)
            except err.HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                return
            except err.URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
                return
            (newStations, newStationsId) = parser.getStationsFromXMLString(xmlString)
            # if something was actually found replace everything
            if newStations:
                # reset id-list
                self.stationId = []
                # clear combo box
                self.railStations.clear()
                # set new id-list
                self.stationId = newStationsId
                # display new station-names
                self.railStations.addItems(newStations)

    def getConnectionsNow(self):
        """
        Encapsulation for requesting connections with system time/date from button.
        Calls getConnectionFromInput with isNow=True.
        """

        self.getConnectionsFromInput(True)

    def getConnectionsWithTime(self):
        """
        Encapsulation for requesting connections with chosen time from button.
        Calls getConnectionFromInput with isNow=False.
        """

        self.getConnectionsFromInput(False)

    def getConnectionsEarlier(self):
        """
        Encapsulation of getting connections with shifted time.
        False indicates earlier. Requesting earlier means subtract
        the shift from the previous time.
        """

        secShift = self.settingsWidget.getOffSet()
        self.getConnectionsWithShiftedTime(False, secShift)

    def getConnectionsLater(self):
        """
        Encapsulation of getting connections with shifted time.
        True indicates later. Requesting later means add
        the shift to the previous time.
        """

        secShift = self.settingsWidget.getOffSet()
        self.getConnectionsWithShiftedTime(True, secShift)

    def getConnectionsWithShiftedTime(self, isShiftPositive: bool, secShift: int):
        """
        Requests connections earlier/later.
        isShiftPositive =False indicates earlier.
        isShiftPositive =True indicates later.
        Base information are read from first connection displayed
        in ConnectionTable.
        """

        # something has to be displayed at the moment or nothing can be read from table
        if self.conList.getDisplayedIndex() >= 0:
            # get the first connection
            con = self.conList.getSingleConnection(self.conList.getDisplayedIndex(), 0)
            # get id, date and time
            identifier = con.stopId
            date = con.date
            time = con.time
            # default set departure
            isDeparture = True
            # direction is not set means it is a arrival
            if con.direction == "":
                isDeparture = False
            # calculate shift (positive or negative depending on isShiftPositive-Flag)
            # calculate possible dayShift
            if isShiftPositive:
                dayShift = 1
                shift = secShift
            else:
                dayShift = -1
                shift = -secShift
            # add shift to requested time
            newTime = time.addSecs(shift)
            # added hours but new Time less than before -> day overflow, thus add one day
            # same for day underflow, subtract one day.
            if (newTime < time and isShiftPositive) or (newTime > time and not isShiftPositive):
                date = date.addDays(dayShift)
            # request new connections
            self.getConnections(date, newTime, identifier, isDeparture)

    def getConnectionsFromInput(self, isNow: bool):
        """
        If isNow is set True gets the current time and date.
        Otherwise reads time and date from userInput.
        Reads all other relevant information (id, isDeparture) from userInput.
        Calls getConnection with these parameters.
        """

        # get selected Index from ComboBox
        index = self.railStations.currentIndex()
        # check invalid Index
        if index < 0:
            return
        # use System-Time
        if isNow:
            # noinspection PyArgumentList
            date = QtCore.QDate.currentDate()
            # noinspection PyArgumentList
            time = QtCore.QTime.currentTime()
        # use selected time from gui
        else:
            time = self.time_chooser.time()
            date = self.date_chooser.selectedDate()
        # get id to selected station
        identifier = self.stationId[index]
        # arrival or departure checked
        if self.arriv.isChecked():
            isDeparture = False
        else:
            isDeparture = True
        self.getConnections(date, time, identifier, isDeparture)

    def getConnections(self, date: QtCore.QDate, time: QtCore.QTime, identifier: int, isDeparture: bool):
        """
         Request the connections from/to (specified by isDeparture flag)
         the train station (specified by identifier) at given Date and Time.
         If request was successful displays requested connection on ConnectionTabel.
         """

        try:
            xmlString = Request.getXMLStringConnectionRequest(date, time, identifier, isDeparture,
                                                              self.settingsWidget.settings)
        except err.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            return
        except err.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            return
        connections = parser.getConnectionsFromXMLString(xmlString, isDeparture)
        self.clearConnectionTable()
        # check if something was actually found
        if not connections:
            # if not set index to last entry of pages so this page can never be reached again
            self.conList.setDisplayedIndex(self.conList.getPageCount() - 1)
            # set connection label to error Message
            self.connection_label.setText(self.errorMsg)
        else:
            self.addConnections(connections)
            # Add list of connections to pages
            self.conList.appendPage(connections)
            # set index to last entry of pages
            self.conList.setDisplayedIndex(self.conList.getPageCount() - 1)
            # set connection label
            self.setConnectionLabel()

    def changePathColor(self):
        """
        Create ColorDialog for choosing path color.
        If valid color is picked, sets the path color
        of settings-object to new color.
        """

        # create ColorDialog
        colorDialog = QtWidgets.QColorDialog()
        # get the color
        newColor = colorDialog.getColor(QtGui.QColor(), self, 'Pfad-Farbe wählen')
        # check for invalid color
        if newColor.isValid():
            self.settingsWidget.settings.setPathColor(newColor)

    def changeMarkerColor(self):
        """
        Create ColorDialog for choosing marker color.
        If valid color is picked, sets the marker color
        of settings-object to new color.
        """

        # create ColorDialog
        colorDialog = QtWidgets.QColorDialog()
        # get the color
        newColor = colorDialog.getColor(QtGui.QColor(), self, 'Marker-Farbe wählen')
        # check for invalid color
        if newColor.isValid():
            self.settingsWidget.settings.setMarkerColor(newColor)

    def showSettingsWidget(self):
        """
        Updates and shows settingsWidget.
        """

        self.settingsWidget.update()

    def keyPressEvent(self, e):
        """
        Basic keyPressEvent for getting connections.
        Enter/return to get stations if none have been
        requested.
        If stations have already been requested enter/return
        to request connections with actual date/time from
        first station.
        All other keyPressEvent are passed to super keyPressEvent.
        """

        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            if not self.stationId:
                self.getStations()
            else:
                self.getConnectionsNow()
        elif e.key() == QtCore.Qt.Key_F5:
            self.refreshPage()
        # pass to the super keyPressEvent
        else:
            super(FormWidget, self).keyPressEvent(e)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    application = FormWidget()
    application.show()
    sys.exit(app.exec_())

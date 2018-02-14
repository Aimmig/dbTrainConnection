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
from Structs import Connection, ConnectionsList, Stop, Filter, Coordinate, RequestSettings, MapType
from XMLParser import XMLParser
import urllib.error as err


class GUI(QtWidgets.QMainWindow):
    """
    Main Gui consist of three parts.
    Part 1 for user input,
    part 2 for displaying general information for connections
    part 3 for displaying detailed information for one connection.
    Additionally holds important global variables.
    """

    def __init__(self):
        """
        Initializes main gui.
        Initializes settings- and mapWidget.
        """

        # super constructor
        # noinspection PyArgumentList
        super(GUI, self).__init__()

        # read all settings information from file including language data
        self.settings = RequestSettings('configs/config.txt')

        # set Window Title
        self.setWindowTitle(self.settings.LanguageStrings.windowTitle_Text)

        # create empty list for station Ids
        self.stationId = []
        # initialize ConnectionList
        self.conList = ConnectionsList()
        # set filter to inactive
        self.filterActive = False
        # initialize Widget for map
        self.mapWidget = QMapWidget()

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

        # create central widget and set layout
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        # create empty Filter
        self.typeFilter = Filter()

        # intialize stuff for default icon
        self.stdicon = self.style().standardIcon
        self.style = QtWidgets.QStyle

        # init Menus
        self.initMenuBar()

    # noinspection PyUnresolvedReferences
    def initMenuBar(self):
        """
        Initializes QMenuBar.
        Adds all needed action for choosing path and marker color etc.
        """

        # get MenuBar
        menuBar = self.menuBar()

        # create Menu for Map
        mapMenu = menuBar.addMenu("Map")

        # create Submenu for changing colors
        mapcolorMenu = mapMenu.addMenu(self.settings.LanguageStrings.colour_Text)

        # submenu entry for changing path colors
        colorPathAction = QtWidgets.QAction(self.stdicon(self.style.SP_DialogOpenButton),
                                            self.settings.LanguageStrings.change_Path_Colour_Text, self)
        colorPathAction.triggered.connect(self.changePathColor)
        mapcolorMenu.addAction(colorPathAction)

        # submenu entry for changing marker colors
        colorMarkerAction = QtWidgets.QAction(self.stdicon(self.style.SP_DialogOpenButton),
                                              self.settings.LanguageStrings.change_Marker_Colour_Text, self)
        colorMarkerAction.triggered.connect(self.changeMarkerColor)
        mapcolorMenu.addAction(colorMarkerAction)

        # add Submenu for changing MapType
        mapTypeMenu = mapMenu.addMenu("Type")

        # create groupAction
        mapGroupAction = QtWidgets.QActionGroup(self)

        # submenu entry for setting roadmap
        roadmapAction = QtWidgets.QAction(MapType.roadmap.name, mapGroupAction)
        roadmapAction.setCheckable(True)
        roadmapAction.triggered.connect(self.setMapType_roadmap)

        # submenu entry for setting sattelitemap
        satelliteAction = QtWidgets.QAction(MapType.satellite.name, mapGroupAction)
        satelliteAction.setCheckable(True)
        satelliteAction.triggered.connect(self.setMapType_satellite)

        # submenu entry for hybridmap
        hybridAction = QtWidgets.QAction(MapType.hybrid.name, mapGroupAction)
        hybridAction.setCheckable(True)
        hybridAction.triggered.connect(self.setMapType_hybrid)

        # submenu entry for terrainmap
        terrainAction = QtWidgets.QAction(MapType.terrain.name, mapGroupAction)
        terrainAction.setCheckable(True)
        terrainAction.triggered.connect(self.setMapType_terrain)

        # try to check default maptype specified in config
        try:
            mapActionDict = {MapType.roadmap: roadmapAction, MapType.satellite: satelliteAction,
                             MapType.hybrid: hybridAction, MapType.terrain: terrainAction}
            mapActionDict[MapType(self.settings.MAPTYPE)].setChecked(True)
        except KeyError:
            pass

        # add all actions from group to menu
        mapTypeMenu.addActions(mapGroupAction.actions())

        # create
        mapSizeMenu = mapMenu.addMenu("Size")

        increaseAction = QtWidgets.QAction(self.stdicon(self.style.SP_ArrowUp), "Increase", self)
        increaseAction.triggered.connect(self.increaseMapSize)
        mapSizeMenu.addAction(increaseAction)

        decreaseAction = QtWidgets.QAction(self.stdicon(self.style.SP_ArrowDown), "Decrease", self)
        decreaseAction.triggered.connect(self.decreaseMapSize)
        mapSizeMenu.addAction(decreaseAction)

        # action for checking Map
        # noinspection PyAttributeOutsideInit
        self.mapActive = QtWidgets.QAction("Anzeigen", self)
        self.mapActive.setCheckable(True)
        self.mapActive.setChecked(True)

        # add map action to menu
        mapMenu.addAction(self.mapActive)

        # create menu for settings
        settingsMenu = menuBar.addMenu("Settings")

        # create submenu for filter
        filterMenu = settingsMenu.addMenu("Filter")
        # create actionGroup for filter
        filterGroupAction = QtWidgets.QActionGroup(self)

        # add action for active filter
        activateFilterAction = QtWidgets.QAction('Aktivieren', filterGroupAction)
        activateFilterAction.setCheckable(True)
        activateFilterAction.setChecked(True)
        activateFilterAction.triggered.connect(self.setFilterActive)

        # add action for inactive filter
        deactiveFilterAction = QtWidgets.QAction('Deaktivieren', filterGroupAction)
        deactiveFilterAction.setCheckable(True)
        deactiveFilterAction.triggered.connect(self.setFilterInactive)

        # add all actions from Fitergroup to menu
        filterMenu.addActions(filterGroupAction.actions())

        # create submenu for offset changing
        searchOffsetMenu = settingsMenu.addMenu("Offset")

        # add action for increase of submenu
        increaseOffsetAction = QtWidgets.QAction(self.stdicon(self.style.SP_ArrowUp), "Increase", self)
        increaseOffsetAction.triggered.connect(self.increaseOffset)
        searchOffsetMenu.addAction(increaseOffsetAction)

        # add action for decrease of submenu
        increaseOffsetAction = QtWidgets.QAction(self.stdicon(self.style.SP_ArrowDown), "Decrease", self)
        increaseOffsetAction.triggered.connect(self.decreaseOffset)
        searchOffsetMenu.addAction(increaseOffsetAction)

        # create Menu for application
        exitMenu = menuBar.addMenu(self.settings.LanguageStrings.application_Text)
        # create Action for closing application
        exitAction = QtWidgets.QAction(self.stdicon(self.style.SP_DialogCancelButton),
                                       self.settings.LanguageStrings.quit_Text, self)
        # connect Action with method
        exitAction.triggered.connect(self.closeEvent)
        # add Action to Menu
        exitMenu.addAction(exitAction)

    # noinspection PyAttributeOutsideInit,PyArgumentList,PyUnresolvedReferences
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
        self.inp.textEdited.connect(self.getStations)

        # group input and button in input_layout1
        input1_layout = QtWidgets.QHBoxLayout()
        input1_layout.addWidget(self.inp)
        # input1_layout.addWidget(self.chooseStation)

        # comboBox for all Stations
        self.railStations = QtWidgets.QComboBox()
        # time chooser for selecting time
        self.time_chooser = QtWidgets.QTimeEdit()
        self.time_chooser.setTime(QtCore.QTime.currentTime())

        # group combo box and time picker in input_layout2
        input2_layout = QtWidgets.QHBoxLayout()
        input2_layout.addWidget(self.railStations)
        input2_layout.addWidget(self.time_chooser)

        # calendar for selecting date
        self.date_chooser = QtWidgets.QCalendarWidget()
        # set language for calender
        self.date_chooser.setLocale(QtCore.QLocale(self.settings.LANGUAGE))
        # initialize Calender with current date
        self.date_chooser.setSelectedDate(QtCore.QDate.currentDate())

        # button for getting connections
        self.request = QtWidgets.QPushButton(self.settings.LanguageStrings.request_Text)
        self.request.clicked.connect(self.getConnectionsByTime)

        # group time_chooser and request in request_layout
        request_layout = QtWidgets.QHBoxLayout()
        # request_layout.addWidget(self.request_now)
        request_layout.addWidget(self.request)

        # create RadioButtons for departure/arrival selection
        self.depart = QtWidgets.QRadioButton(self.settings.LanguageStrings.departure_Text)
        self.arriv = QtWidgets.QRadioButton(self.settings.LanguageStrings.arrival_Text)
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
        # create CheckBoxes for choosing filters
        self.checkICE = QtWidgets.QCheckBox(self.settings.LanguageStrings.ICE_Text)
        self.checkIC = QtWidgets.QCheckBox(self.settings.LanguageStrings.IC_Text)
        self.checkOther = QtWidgets.QCheckBox(self.settings.LanguageStrings.other_Text)
        # add checkboxes to filterLayout
        filterLayout.addWidget(self.checkICE)
        filterLayout.addWidget(self.checkIC)
        filterLayout.addWidget(self.checkOther)

        # create global Layout
        propertiesLayout = QtWidgets.QHBoxLayout()

        # create buttons for getting connections earlier/later and group them
        requestEarlierLater_layout = QtWidgets.QHBoxLayout()
        self.earlier = QtWidgets.QPushButton(self.settings.LanguageStrings.earlier_Text)
        self.later = QtWidgets.QPushButton(self.settings.LanguageStrings.later_Text)
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
        layout.addLayout(propertiesLayout)
        layout.addLayout(requestEarlierLater_layout)
        layout.addLayout(request_layout)

        return layout

    # noinspection PyAttributeOutsideInit,PyArgumentList,PyUnresolvedReferences
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
        self.prev = QtWidgets.QPushButton(self.settings.LanguageStrings.previous_Text)
        self.prev.clicked.connect(self.showPreviousPage)
        # button for refreshing the page using new filter
        self.reload = QtWidgets.QPushButton(self.settings.LanguageStrings.refresh_Text)
        self.reload.clicked.connect(self.refreshPage)
        # button for navigating
        self.next = QtWidgets.QPushButton(self.settings.LanguageStrings.next_Text)
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

    # noinspection PyArgumentList,PyAttributeOutsideInit,PyUnresolvedReferences
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

        # close map
        self.mapWidget.close()

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
                self.details_label.setText(e.code)
                return
            except err.URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
                self.details_label.setText(str(e.reason))
                return
            stopList = XMLParser.getStopListFromXMLString(xmlString)
            if stopList:
                # set the stopList of the connection to the local list
                connection.stopList = stopList
            else:
                self.clearDetailsTable()
                self.details_label.setText(self.settings.LanguageStrings.errorMsg)
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
        sett = self.settings
        # set details_label text to connection information
        self.details_label.setText(connection.toStringDetails(sett))
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
        if (connection.imageData.isEmpty() or self.settings.MAPTYPE != connection.mapType) \
                and self.mapActive.isChecked():
            # request imageData and create QByteArray and set imageData
            # noinspection PyArgumentList,PyTypeChecker
            connection.imageData = QtCore.QByteArray(
                Request.getMapWithLocations(coordinates, markerIndex, self.settings))
            connection.mapType = self.settings.MAPTYPE
        # display requested map-Data
        if self.mapActive.isChecked():
            self.mapWidget.showMap(connection.imageData, connection.toStringDetails(self.settings) + ' (' + MapType(
                connection.mapType).name + ')')

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

        ICE = self.checkICE.isChecked()
        IC = self.checkIC.isChecked()
        Other = self.checkOther.isChecked()
        # minimum one filter type must be selected
        self.filterActive = ICE or IC or Other
        # add all connections to table
        for c in connections:
            self.addConnectionToTable(c)
        # displayed connections shall be filtered
        if self.filterActive:
            self.typeFilter = Filter(ICE, IC, Other)
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
        sett = self.settings
        self.connection_label.setText(
            self.conList.getSingleConnection(self.conList.getDisplayedIndex(), 0).toStringGeneral(sett))

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
        sett = self.settings
        self.connectionTable.setItem(row, QConnectionTable.time_Index,
                                     QtWidgets.QTableWidgetItem(con.timeToString(sett)))
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
        sett = self.settings
        if stop.arrTime:
            self.detailsTable.setItem(row, QDetailsTable.arr_Index,
                                      QtWidgets.QTableWidgetItem(stop.arrTimeToString(sett)))
        if stop.depTime:
            self.detailsTable.setItem(row, QDetailsTable.dep_Index,
                                      QtWidgets.QTableWidgetItem(stop.depTimeToString(sett)))
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
                xmlString = Request.getXMLStringStationRequest(loc, self.settings)
            except err.HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                self.railStations.clear()
                self.railStations.addItem(e.code)
                return
            except err.URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
                self.railStations.clear()
                self.railStations.addItem(str(e.reason))
                return
            (newStations, newStationsId) = XMLParser.getStationsFromXMLString(xmlString)
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

    def getConnectionsEarlier(self):
        """
        Encapsulation of getting connections with shifted time.
        False indicates earlier. Requesting earlier means subtract
        the shift from the previous time.
        """

        secShift = self.settings.getOffSet()
        self.getConnectionsWithShiftedTime(False, secShift)

    def getConnectionsLater(self):
        """
        Encapsulation of getting connections with shifted time.
        True indicates later. Requesting later means add
        the shift to the previous time.
        """

        secShift = self.settings.getOffSet()
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

    def getConnectionsByTime(self):
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
            xmlString = Request.getXMLStringConnectionRequest(date, time, identifier, isDeparture, self.settings)
        except err.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            self.connection_label.setText(e.code)
            return
        except err.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            self.connection_label.setText(str(e.reason))
            return
        connections = XMLParser.getConnectionsFromXMLString(xmlString, isDeparture)
        self.clearConnectionTable()
        # check if something was actually found
        if not connections:
            # if not set index to last entry of pages so this page can never be reached again
            self.conList.setDisplayedIndex(self.conList.getPageCount() - 1)
            # set connection label to error Message
            self.connection_label.setText(self.settings.LanguageStrings.errorMsg)
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
        newColor = colorDialog.getColor(QtGui.QColor(), self, self.settings.LanguageStrings.select_Path_Colour_Text)
        # check for invalid color
        if newColor.isValid():
            self.settings.setPathColor(newColor)

    def changeMarkerColor(self):
        """
        Create ColorDialog for choosing marker color.
        If valid color is picked, sets the marker color
        of settings-object to new color.
        """

        # create ColorDialog
        colorDialog = QtWidgets.QColorDialog()
        # get the color
        newColor = colorDialog.getColor(QtGui.QColor(), self, self.settings.LanguageStrings.select_Marker_Colour_Text)
        # check for invalid color
        if newColor.isValid():
            self.settings.setMarkerColor(newColor)

    def increaseMapSize(self):
        """
        TO-DO
        """
        print("INC-MAP")

    def decreaseMapSize(self):
        """
        TO-DO
        """
        print("DEC-MAP")

    def increaseOffset(self):
        """
        TO-DO
        """
        print("INC-OFFSET")

    def decreaseOffset(self):
        """
        TO-DO
        """
        print("DEC-OFFSET")

    def setFilterActive(self):
        """
        Make all Filters checkable
        """
        self.checkICE.setCheckable(True)
        self.checkIC.setCheckable(True)
        self.checkOther.setCheckable(True)

    def setFilterInactive(self):
        """
        Deselect all Filters and make them not checkable
        """
        self.checkICE.setChecked(False)
        self.checkICE.setCheckable(False)
        self.checkIC.setChecked(False)
        self.checkIC.setCheckable(False)
        self.checkOther.setChecked(False)
        self.checkOther.setCheckable(False)

    def setMapType_roadmap(self):
        """
        Set Maptype value to roadmap
        """
        self.settings.MAPTYPE = MapType.roadmap.value

    def setMapType_satellite(self):
        """
        Set Maptype value to satelitte
        """
        self.settings.MAPTYPE = MapType.satellite.value

    def setMapType_hybrid(self):
        """
        Set Maptype to hybrid
        """
        self.settings.MAPTYPE = MapType.hybrid.value

    def setMapType_terrain(self):
        """
        Set Mapytpe to terrain
        """
        self.settings.MAPTYPE = MapType.terrain.value

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
                self.getConnectionsByTime()
        elif e.key() == QtCore.Qt.Key_F5:
            self.refreshPage()
        # pass to the super keyPressEvent
        else:
            super(GUI, self).keyPressEvent(e)

    # Quit Action
    def closeEvent(self, evt):
        # close MapWidget
        self.mapWidget.close()
        # close Formwidget
        super(GUI, self).close()

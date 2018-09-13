#    -----------------------------------------------------------------------
#    This program requests connections and corresponding details from the
#    API of Deutsche Bahn and presents them in an user interface
#    This file encapsulates 2 subWidgets (QTables) with special properties,
#    for displaying connection or details and a widget for displaying the map. 
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

from PyQt5 import QtWidgets, QtCore, QtGui


class Table(QtWidgets.QTableWidget):

    def __init__(self, main, child, header_list):
        super(Table, self).__init__()
        self.mainWidget = main
        # set columnCount to number of entries in header list
        self.setColumnCount(len(header_list))
        # set Horizontal Header for QTableWidget
        self.setHorizontalHeaderLabels(header_list)
        # make table not editable
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # make only rows selectable
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # only one selection at a time is allowed
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # do not show grind
        self.setShowGrid(False)
        # set minimum Size
        self.setMinimumSize(QtCore.QSize(child.minimumWidth, child.minimumHeight))
        # set size policy to minimalExpanding
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

    def prepareHeader(self, main):
        raise NotImplementedError("Please Implement this method")

    def resizingHeader(self):
        raise NotImplementedError("Please Implement this method")

    def sort(self, index):
        raise NotImplementedError("Please Implement this method")

    @staticmethod
    def stretchHeader(header, index):
        header.setSectionResizeMode(index, QtWidgets.QHeaderView.Stretch)

    @staticmethod
    def resizeHeaderToContents(header, index):
        header.setSectionResizeMode(index, QtWidgets.QHeaderView.ResizeToContents)

    @staticmethod
    def setUpHeader(headerList, index, text):
        headerList[index] = text

    @staticmethod
    def initHeaderList(length):
        return ['']*length


class QConnectionTable(Table):
    """
    Class QConnection is derived from QTableWidget.
    Used for displaying connections on gui.
    Encapsulates all settings in constructor.
    Defines some new keyPressEvents.
    """

    # define some constants for later use
    name_Index = 0
    from_Index = 1
    to_Index = 2
    time_Index = 3
    track_Index = 4
    header_list_length = 5

    minimumWidth = 420
    minimumHeight = 320

    def __init__(self, main):
        """
        Initializes QConnectionTable.
        Sets all desired properties.
        Sets appropriates headers.
        :type main FormWidget
        """

        header_list = self.prepareHeader(main)
        # call super constructor
        super().__init__(main, QConnectionTable, header_list)
        # do not show vertical Header
        self.verticalHeader().setVisible(False)
        self.resizingHeader()
        self.horizontalHeader().sectionDoubleClicked.connect(self.sort)

    def prepareHeader(self, main):
        header_list = Table.initHeaderList(QConnectionTable.header_list_length)
        Table.setUpHeader(header_list, QConnectionTable.from_Index, main.settings.LanguageStrings.from_Text)
        Table.setUpHeader(header_list, QConnectionTable.to_Index, main.settings.LanguageStrings.to_Text)
        Table.setUpHeader(header_list, QConnectionTable.time_Index, main.settings.LanguageStrings.time_Text)
        Table.setUpHeader(header_list, QConnectionTable.name_Index, main.settings.LanguageStrings.name_Text)
        Table.setUpHeader(header_list, QConnectionTable.track_Index, main.settings.LanguageStrings.track_Text)
        return header_list

    def resizingHeader(self):
        # set all Columns to ResizeToContent
        # only columns with stop names are allowed to stretch
        Table.resizeHeaderToContents(self.horizontalHeader(), QConnectionTable.name_Index)
        Table.stretchHeader(self.horizontalHeader(), QConnectionTable.from_Index)
        Table.stretchHeader(self.horizontalHeader(), QConnectionTable.to_Index)
        Table.resizeHeaderToContents(self.horizontalHeader(), QConnectionTable.time_Index)
        Table.resizeHeaderToContents(self.horizontalHeader(), QConnectionTable.track_Index)

    def keyPressEvent(self, e):
        """
        Defines keyPress Events for QConnectionTable.
        Enter or return trigger request of details (like mouseClick).
        Left or right arrow used for navigation in connectionPages.
        All other events are passed to super keyPressEvent.
        """

        # enter/return key triggers details
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.mainWidget.getDetails()
        # left key shows previous page
        elif e.key() == QtCore.Qt.Key_Left:
            self.mainWidget.showPreviousPage()
        # right key shows next page
        elif e.key() == QtCore.Qt.Key_Right:
            self.mainWidget.showNextPage()
        # pass to the super keyPressEvent
        else:
            super(QConnectionTable, self).keyPressEvent(e)

    def sort(self, index):
        if index != QConnectionTable.track_Index:
            self.sortItems(index)


class QDetailsTable(Table):
    """
    Class QDetailsTable is derived from QTableWidget.
    Used for displaying connection-details on gui.
    Encapsulates all settings in constructor.
    Defines some new keyPressEvents.
    """

    # define some constants for later use
    stop_Index = 0
    arr_Index = 1
    dep_Index = 2
    track_Index = 3
    header_list_length = 4

    minimumWidth = 420
    minimumHeight = 320

    def __init__(self, main):
        """
        Initializes QDetailsTable.
        Sets all desired properties.
        Sets appropriates headers.
        :type main FormWidget
        """

        header_list = self.prepareHeader(main)
        super().__init__(main, QDetailsTable, header_list)
        self.resizingHeader()
        self.horizontalHeader().sectionDoubleClicked.connect(self.sort)

    def prepareHeader(self, main):
        header_list = Table.initHeaderList(QDetailsTable.header_list_length)
        Table.setUpHeader(header_list, QDetailsTable.stop_Index, main.settings.LanguageStrings.stop_Text)
        Table.setUpHeader(header_list, QDetailsTable.arr_Index, main.settings.LanguageStrings.arrival_Text)
        Table.setUpHeader(header_list, QDetailsTable.dep_Index, main.settings.LanguageStrings.departure_Text)
        Table.setUpHeader(header_list, QDetailsTable.track_Index, main.settings.LanguageStrings.track_Text)
        return header_list

    def resizingHeader(self,):
        # only stretch column with stop, resize other columns to contents
        Table.stretchHeader(self.horizontalHeader(), QDetailsTable.stop_Index)
        Table.resizeHeaderToContents(self.horizontalHeader(), QDetailsTable.arr_Index)
        Table.resizeHeaderToContents(self.horizontalHeader(), QDetailsTable.dep_Index)
        Table.resizeHeaderToContents(self.horizontalHeader(), QDetailsTable.track_Index)

    def keyPressEvent(self, e):
        """
        Defines keyPress Events for QDetailsTable.
        Enter or return trigger request of connection (like mouseClick).
        All other events are passed to super keyPressEvent.
        """

        # enter/return triggers getConnections
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            self.mainWidget.getConnectionsOnClickInDetails()
        # Pass to the super keyPressEvent
        else:
            super(QDetailsTable, self).keyPressEvent(e)

    def sort(self, index):
        if index != QDetailsTable.track_Index:
            self.sortItems(index)


class QMapWidget(QtWidgets.QWidget):
    """
    Class QMapWidget is derived from QWidget.
    Used for displaying an additional requested map.
    Defines method to set and show the map.
    Constructor encapsulates some basic settings.
    """

    def __init__(self):
        """
        Initializes Widget.
        Sets some properties like layout, etc.
        """

        super().__init__()
        # set label to Widget
        self.mapLabel = QtWidgets.QLabel()
        self.mapLabel.setScaledContents(True)
        # set layout of widget
        mapLayout = QtWidgets.QVBoxLayout()
        mapLayout.addWidget(self.mapLabel)
        self.setLayout(mapLayout)
        # make widget not resizable
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

    def showMap(self, imageData: QtCore.QByteArray(), windowTitle: str):
        """
        Loads the (raw) imageData to pixMap.
        Sets the windowTitle to given value and
        shows widget.
        :type imageData QtCore.QByteArray
        :type windowTitle str
        """

        # create pixMap
        pixMap = QtGui.QPixmap()
        # try to load imageData to pixMap
        if pixMap.loadFromData(imageData):
            # set window title
            self.setWindowTitle(windowTitle)
            # put pixMap on label
            self.mapLabel.setPixmap(pixMap)
            # show widget
            self.show()

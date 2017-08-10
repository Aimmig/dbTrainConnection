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


class QConnectionTable(QtWidgets.QTableWidget):
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
    header_list = ['Zugnummer', 'von', 'nach', 'Uhrzeit', 'Gleis']
    minimumWidth = 420
    minimumHeight = 320

    def __init__(self, main):
        """
        Initializes QConnectionTable.
        Sets all desired properties.
        Sets appropriates headers.
        :type main FormWidget
        """

        # call super constructor
        super(QConnectionTable, self).__init__()
        # set mainWidget to main
        self.mainWidget = main
        # set columnCount to number of entries in header list
        self.setColumnCount(len(QConnectionTable.header_list))
        # set Horizontal Header for QTableWidget
        self.setHorizontalHeaderLabels(QConnectionTable.header_list)
        # make table not editable
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # only make rows selectable
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # only one selection at a time is allowed
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # do not show grind
        self.setShowGrid(False)
        # do not show vertical Header
        self.verticalHeader().setVisible(False)
        header = self.horizontalHeader()
        # set all Columns to ResizeToContent
        # only columns with stop names are allowed to stretch
        header.setSectionResizeMode(QConnectionTable.name_Index, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(QConnectionTable.from_Index, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(QConnectionTable.to_Index, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(QConnectionTable.time_Index, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(QConnectionTable.track_Index, QtWidgets.QHeaderView.ResizeToContents)
        # set MinimumSize
        self.setMinimumSize(QtCore.QSize(QConnectionTable.minimumWidth, QConnectionTable.minimumHeight))
        # set Size Policy to MinimumExpanding
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

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


class QDetailsTable(QtWidgets.QTableWidget):
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
    header_list = ['Halt', 'Ankunft', 'Abfahrt', 'Gleis']
    minimumWidth = 420
    minimumHeight = 320

    def __init__(self, main):
        """
        Initializes QDetailsTable.
        Sets all desired properties.
        Sets appropriates headers.
        :type main FormWidget
        """

        # call super constructor
        super(QDetailsTable, self).__init__()
        # set mainWidget to main
        self.mainWidget = main
        # make table not editable
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # make only rows selectable
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # make only one row selectable at a time
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # set numberColumnCount to length of header
        self.setColumnCount(len(QDetailsTable.header_list))
        # set Horizontal Headers
        self.setHorizontalHeaderLabels(QDetailsTable.header_list)
        header = self.horizontalHeader()
        # only stretch column with stop, resize other columns to contents
        header.setSectionResizeMode(QDetailsTable.stop_Index, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(QDetailsTable.arr_Index, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(QDetailsTable.dep_Index, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(QDetailsTable.track_Index, QtWidgets.QHeaderView.ResizeToContents)
        # do not show grid
        self.setShowGrid(False)
        # set minimum Size
        self.setMinimumSize(QtCore.QSize(QDetailsTable.minimumWidth, QDetailsTable.minimumHeight))
        # set size policy to minimalExpanding
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

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


class QMapWidget(QtWidgets.QWidget):
    """
    Class QMapWidget is derived from QWidget.
    Used for displaying an additional requested map.
    Defines method to set and show the map.
    Constructor encapsulates some basic settings.
    """

    # noinspection PyArgumentList
    def __init__(self):
        """
        Initializes Widget.
        Sets some properties like layout, etc.
        """

        super(QMapWidget, self).__init__()
        # set label to Widget
        self.mapLabel = QtWidgets.QLabel()
        self.mapLabel.setScaledContents(True)
        # set layout of widget
        mapLayout = QtWidgets.QVBoxLayout()
        mapLayout.addWidget(self.mapLabel)
        self.setLayout(mapLayout)

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

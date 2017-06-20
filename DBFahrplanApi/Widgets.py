#    -----------------------------------------------------------------------
#    This programm requests connections and corresponding details from the
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

from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg

class QConnectionTable(qw.QTableWidget):
        """
        Class QConnection is derived from QTableWidget.
        Used for displaying connections on gui.
        Encapsulates all settings in constructor.
        Defines some new keyPressEvents.
        """

        #define some constants for later use
        name_Index=0
        from_Index=1
        to_Index=2
        time_Index=3
        track_Index=4
        header_list=["Zugnummer","von","nach","Uhrzeit","Gleis"]
        minimumWidth=420
        minimumHeight=320

        def __init__(self,main):
                """
                Initializes QConnectionTable.
                Sets all desired properties.
                Sets appropiates headers.
                """

                #call super constructor
                super(QConnectionTable,self).__init__()
                #set mainWidget to main
                self.mainWidget=main
                #set columCount to number of entries in header list
                self.setColumnCount(len(QConnectionTable.header_list))
                #set Horizontal Header for QTableWidget
                self.setHorizontalHeaderLabels(QConnectionTable.header_list)
                #make table not editable
                self.setEditTriggers(qw.QAbstractItemView.NoEditTriggers)
                #only make rows selectable
                self.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
                #only one selection at a time is allowed
                self.setSelectionMode(qw.QAbstractItemView.SingleSelection)
                #do not show grind
                self.setShowGrid(False)
                #do not show vertical Header
                self.verticalHeader().setVisible(False)
                header=self.horizontalHeader()
                #set all Columns to ResizeToConents 
                #only colums with stop names are allowed to stretch
                header.setSectionResizeMode(QConnectionTable.name_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(QConnectionTable.from_Index,qw.QHeaderView.Stretch)
                header.setSectionResizeMode(QConnectionTable.to_Index,qw.QHeaderView.Stretch)
                header.setSectionResizeMode(QConnectionTable.time_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(QConnectionTable.track_Index,qw.QHeaderView.ResizeToContents)
                #set MimimumSize
                self.setMinimumSize(qc.QSize(QConnectionTable.minimumWidth,QConnectionTable.minimumHeight))
                #set Size Policy to MimumExpanding
                self.setSizePolicy(qw.QSizePolicy.MinimumExpanding,qw.QSizePolicy.MinimumExpanding)

        def keyPressEvent(self,e):
                """
                Defines keyPress Events for QConnectionTable.
                Enter or return trigger request of details (like mouseclick).
                Left or right arrow used for navigation in connectionPages.
                All other events are passed to super keyPressEvent.
                """
                
                #enter/return key triggers details
                if e.key() == qc.Qt.Key_Return or e.key()==qc.Qt.Key_Enter:
                        self.mainWidget.getDetails()
                #left key shows previous page
                elif e.key() == qc.Qt.Key_Left:
                        self.mainWidget.showPreviousPage()
                #right key shows next page
                elif e.key() == qc.Qt.Key_Right:
                        self.mainWidget.showNextPage()
                #pass to the super keyPressEvent
                else:
                       super(QConnectionTable,self).keyPressEvent(e)

class QDetailsTable(qw.QTableWidget):
        """
        Class QDetailsTable is derived from QTableWidget.
        Used for displaying connection-details on gui.
        Encapsulates all settings in constructor.
        Defines some new keyPressEvents.
        """

        #define some constants for later use
        stop_Index=0
        arr_Index=1
        dep_Index=2
        track_Index=3
        header_list=["Halt","Ankunft","Abfahrt","Gleis"]
        minimumWidth=420
        minimumHeight=320

        def __init__(self,main):
                """
                Initializes QDetailsTable.
                Sets all desired properties.
                Sets appropiates headers.
                """
                
                #call super constructor
                super(QDetailsTable,self).__init__()
                #set mainWidget to main
                self.mainWidget=main
                #make table not editable
                self.setEditTriggers(qw.QAbstractItemView.NoEditTriggers)
                #make only rows selectable
                self.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
                #make only one row selectable at a time
                self.setSelectionMode(qw.QAbstractItemView.SingleSelection)
                #set numberColumnCount to length of header
                self.setColumnCount(len(QDetailsTable.header_list))
                #set Horizontal Headers
                self.setHorizontalHeaderLabels(QDetailsTable.header_list)
                header=self.horizontalHeader()
                #only stretch colum with stop, resize other columns to contents
                header.setSectionResizeMode(QDetailsTable.stop_Index,qw.QHeaderView.Stretch)
                header.setSectionResizeMode(QDetailsTable.arr_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(QDetailsTable.dep_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(QDetailsTable.track_Index,qw.QHeaderView.ResizeToContents)
                #do not show grid
                self.setShowGrid(False)
                #set minimum Size
                self.setMinimumSize(qc.QSize(QDetailsTable.minimumWidth,QDetailsTable.minimumHeight))
                #set size policy to minimalExpanding
                self.setSizePolicy(qw.QSizePolicy.MinimumExpanding,qw.QSizePolicy.MinimumExpanding)

        def keyPressEvent(self,e):
                """
                Defines keyPress Events for QDetailsTable.
                Enter or return trigger request of connection (like mouseclick).
                All other events are passed to super keyPressEvent.
                """
                #enter/return triggers getConnections
                if e.key() == qc.Qt.Key_Return or e.key()==qc.Qt.Key_Enter:
                        self.mainWidget.getConnectionsOnClickInDetails()
                #Pass to the super keyPressEvent
                else:
                        super(QDetailsTable,self).keyPressEvent(e)

class QMapWidget(qw.QWidget):
      """
      Class QMapWidget is derived from QWidget.
      Used for displaying an additionaly requested map.
      Defines method to set and show the map.
      Constructor encapsulates some basic settings.
      """

      def __init__(self):
           """
           Initalizes Widget.
           Sets some properties like layout, etc.
           """

           super(QMapWidget,self).__init__()
           #set label to Widget
           self.mapLabel=qw.QLabel()
           self.mapLabel.setScaledContents(True)
           #set layout of widget
           mapLayout=qw.QVBoxLayout()
           mapLayout.addWidget(self.mapLabel)
           self.setLayout(mapLayout)

      def showMap(self,imageData,windowTitle):
           """
           Loads the (raw) imageData to pixmap.
           Sets the windowTitle to given value and
           shows widget.
           """
           #create Pixmap
           pixmap=qg.QPixmap()
           #try to load imageData to pixmap
           if pixmap.loadFromData(imageData):
                #set window title
                self.setWindowTitle(windowTitle)
                #put pixmap on label
                self.mapLabel.setPixmap(pixmap)
                #show widget
                self.show()
                

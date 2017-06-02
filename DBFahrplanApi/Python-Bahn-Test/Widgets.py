from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg

#class is a QTableWidget with special properties for displaying Connections
class QConnectionTable(qw.QTableWidget):

        #define some constants for later use
        name_Index=0
        from_Index=1
        to_Index=2
        time_Index=3
        track_Index=4
        header_list=["Zugnummer","von","nach","Uhrzeit","Gleis"]
        minimumWidth=420
        minimumHeight=320
       
        #constructor sets all needed properties
        def __init__(self,main):

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

        #overwrite keyPressEvent
        def keyPressEvent(self,e):
                #enter/return key triggers details
                if e.key() == qc.Qt.Key_Return or e.key()==qc.Qt.Key_Enter:
                        self.mainWidget.getDetails()
                #left key shows previous page
                elif e.key() == qc.Qt.Key_Left:
                        self.mainWidget.showPreviousPage()
                #right key shows next page
                elif e.key() == qc.Qt.Key_Right:
                        self.mainWidget.showNextPage()
                #all other events are passed to the super keyPressEvent
                else:
                       super(QConnectionTable,self).keyPressEvent(e)

#class is a QTableWidget with special properties for displaying ConnectionDetails
class QDetailsTable(qw.QTableWidget):

        #define some constants for later use
        stop_Index=0
        arr_Index=1
        dep_Index=2
        track_Index=3
        header_list=["Halt","Ankunft","Abfahrt","Gleis"]
        minimumWidth=420
        minimumHeight=320

        #constructor sets  all needed properties
        def __init__(self,main):
                
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

        #overwrite keyPressEvent
        def keyPressEvent(self,e):
                #enter/return triggers getConnections
                if e.key() == qc.Qt.Key_Return or e.key()==qc.Qt.Key_Enter:
                        self.mainWidget.getConnectionsOnClickInDetails()
                #all other events are passed to the super keyPressEvent
                else:
                        super(QDetailsTable,self).keyPressEvent(e)

#class for encapsulationg Widget for displaying map
class QMapWidget(qw.QWidget):

      #constructor
      def __init__(self):

           super(QMapWidget,self).__init__()
           #set label to Widget
           self.mapLabel=qw.QLabel()
           self.mapLabel.setScaledContents(True)
           #set layout of widget
           mapLayout=qw.QVBoxLayout()
           mapLayout.addWidget(self.mapLabel)
           self.setLayout(mapLayout)

      #shows map from given data and sets windowTitle
      def showMap(self,imageData,windowTitle):
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
                

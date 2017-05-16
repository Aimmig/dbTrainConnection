import sys
import time as tm

#import qt-stuff
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

from Connection import Connection
from Stop import Stop

#import class for requests
import Request as req
#import class for parsing xml-String
import XMLParser as parser

details_stop_Index=0
details_arr_Index=1
details_dep_Index=2
details_track_Index=3
header_details_list=["Halt","Ankunft","Abfahrt","Gleis"]
connection_name_Index=0
connection_from_Index=1
connection_to_Index=2
connection_time_Index=3
connection_track_Index=4
header_list=["Zugnummer","von","nach","Uhrzeit","Gleis"]
minimumWidth=420
minimumHeight=320
start_x_pos=100
start_y_pos=100


#Class that defines gui
class FormWidget(qw.QWidget):

    #constructor for gui
    def __init__(self):

        #super constructor
        super(FormWidget,self).__init__()
        
        #set some properties
        self.setAutoFillBackground(True)
        self.setWindowTitle("Fahrplanzeige")
        self.errorMsg="Keine Verbindungen gefunden"
        self.stationId=[]
        self.connectionPages=[]
        self.displayedIndex=-1
        self.displayedDetailedIndex=(-1,-1)

        #overall layout for gui 
        layout=qw.QHBoxLayout()

        #layout for left part of gui
        box1=qw.QVBoxLayout()

        #input field for user input
        self.inp=qw.QLineEdit()
        #button for getting stations
        self.chooseStation=qw.QPushButton("Bahnhof wählen")
        self.chooseStation.clicked.connect(self.getStations)

        #group input and button in input_layout1
        input1_layout=qw.QHBoxLayout()
        input1_layout.addWidget(self.inp)
        input1_layout.addWidget(self.chooseStation)

        #comboBox for all Stations
        self.railStations=qw.QComboBox()
        #time chooser for selecting time
        self.time_chooser=qw.QTimeEdit()
        
        #group combo box and time picker in input_layout2
        input2_layout=qw.QHBoxLayout()
        input2_layout.addWidget(self.railStations)
        input2_layout.addWidget(self.time_chooser)
        
        #calendar for selecting date
        self.date_chooser=qw.QCalendarWidget()

        #buttons for getting all connections with System Time
        self.request_now=qw.QPushButton("Jetzt") 
        self.request_now.clicked.connect(self.getConnectionsNow)
        #button for getting connections with choosen Time
        self.request_choosenTime=qw.QPushButton("Anfragen")
        self.request_choosenTime.clicked.connect(self.getConnectionsWithTime)

        #group time_chooser and request in request_layout
        request_layout=qw.QHBoxLayout()
        request_layout.addWidget(self.request_now)
        request_layout.addWidget(self.request_choosenTime)

        #create RadioButtons for departure/arrival selection
        self.depart=qw.QRadioButton("Departure")
        self.arriv=qw.QRadioButton("Arrival")
        #group RadioButtons
        radioButton_layout=qw.QHBoxLayout()
        radioButton_layout.addWidget(self.depart)
        radioButton_layout.addWidget(self.arriv)
        #make RadioButtons checkable and set departure to default checked
        self.depart.setCheckable(True)
        self.arriv.setCheckable(True)
        self.depart.setChecked(True)
        
        #create buttons for getting connections earlier/later and group them
        requestEarlierLater_layout=qw.QHBoxLayout()
        self.earlier=qw.QPushButton("Früher")
        self.later=qw.QPushButton("Später")
        self.later.clicked.connect(self.getConnectionsLater)
        self.earlier.clicked.connect(self.getConnectionsEarlier)
        requestEarlierLater_layout.addWidget(self.earlier)
        requestEarlierLater_layout.addWidget(self.later)
        
        #add layouts and widgets to layout for left part
        box1.addLayout(input1_layout)
        box1.addLayout(input2_layout)
        box1.addWidget(self.date_chooser)
        box1.addLayout(radioButton_layout)
        box1.addLayout(request_layout)
        box1.addLayout(requestEarlierLater_layout)

        #layout for middle part of gui
        box2=qw.QVBoxLayout()

        #label for connection list
        self.connection_label=qw.QLabel("")
        #QTableWidget for displaying connections
        self.connection_list=qw.QTableWidget()
        #use 5 columns to present data
        self.connection_list.setColumnCount(5)
        #set Horizontal Header for QTableWidget
        
        self.connection_list.setHorizontalHeaderLabels(header_list)
        #make table not editable
        self.connection_list.setEditTriggers(qw.QAbstractItemView.NoEditTriggers)
        #only make rows selectable
        self.connection_list.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
        #only one selection at a time is allowed
        self.connection_list.setSelectionMode(qw.QAbstractItemView.SingleSelection)
        #do not show grind and vertical Headers
        self.connection_list.setShowGrid(False)
        self.connection_list.verticalHeader().setVisible(False)
        header=self.connection_list.horizontalHeader()
        header.setSectionResizeMode(connection_name_Index,qw.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(connection_from_Index,qw.QHeaderView.Stretch)
        header.setSectionResizeMode(connection_to_Index,qw.QHeaderView.Stretch)
        header.setSectionResizeMode(connection_time_Index,qw.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(connection_track_Index,qw.QHeaderView.ResizeToContents)
        self.connection_list.setMinimumSize(qc.QSize(minimumWidth,minimumHeight))
        self.connection_list.setSizePolicy(qw.QSizePolicy.MinimumExpanding,qw.QSizePolicy.MinimumExpanding)
        #connect QTableWidget with function
        self.connection_list.clicked.connect(self.getDetails)
        
        #button for navigating
        self.prev=qw.QPushButton("Vorherige")
        self.prev.clicked.connect(self.showPreviousPage)
        #button for navigating
        self.next=qw.QPushButton("Nächste")
        self.next.clicked.connect(self.showNextPage)

        #layout for connection_list navigation
        navigation_layout=qw.QHBoxLayout()
        #add buttons to navigation layout        
        navigation_layout.addWidget(self.prev)
        navigation_layout.addWidget(self.next)
         
        #add widgets and layouts to layout for middle part
        box2.addWidget(self.connection_label)
        box2.addWidget(self.connection_list)
        box2.addLayout(navigation_layout)
        
        #layout for right part of gui
        box3=qw.QVBoxLayout()
        
        #label for details of a connection
        self.details_label=qw.QLabel("")
        #QTableWidget for presenting detailed data of a connection
        self.connection_details=qw.QTableWidget()
        #make table not editable
        self.connection_details.setEditTriggers(qw.QAbstractItemView.NoEditTriggers)
        #make only rows selectable
        self.connection_details.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
        #make only one row selectable at a time
        self.connection_details.setSelectionMode(qw.QAbstractItemView.SingleSelection)
        #use for columns to present data
        self.connection_details.setColumnCount(4)
        #set Horizontal Headers for QTableWidget
        self.connection_details.setHorizontalHeaderLabels(header_details_list)
        header=self.connection_details.horizontalHeader()
        #only stretch first colum, resize other columns to contents
        header.setSectionResizeMode(details_stop_Index,qw.QHeaderView.Stretch)
        header.setSectionResizeMode(details_arr_Index,qw.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(details_dep_Index,qw.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(details_track_Index,qw.QHeaderView.ResizeToContents)
        #do not show grid
        self.connection_details.setShowGrid(False)
        self.connection_details.setMinimumSize(qc.QSize(minimumWidth,minimumHeight))
        #set size policy to minimalExpanding
        self.connection_details.setSizePolicy(qw.QSizePolicy.MinimumExpanding,qw.QSizePolicy.MinimumExpanding)
        #connect QTableWidget with function
        self.connection_details.clicked.connect(self.getConnectionsOnClickInDetails)
        
        #add label to box3
        box3.addWidget(self.details_label)
        #add QTableWidget to box3
        box3.addWidget(self.connection_details)
 
        #add all layouts to form-Layout
        layout.addLayout(box1)
        layout.addLayout(box2)
        layout.addLayout(box3)
        
        #set formLayout
        self.setLayout(layout)
        
    #called on click of connection_details
    def getConnectionsOnClickInDetails(self):
        #get selected Row in connection details
        row=self.connection_details.currentRow()
        #get the displayedIndex Information
        (pageIndex,connectionIndexOnPage)=self.displayedIndexDetails
        #select the clicked stop from the displayed Connection (Details)
        s=self.connectionPages[pageIndex][connectionIndexOnPage].stopList[row]
        #default use arrival Date and Time
        date=s.arrDate
        time=s.arrTime
        #if date or time are invalid try using depDate/time 
        if not date or not time:
              date=s.depDate
              time=s.depTime
        identifier=s.id
        #request information and display it
        self.getConnections(date,time,identifier,True)
    
    #called on click of connection_list
    #request connection details if needed and displays them  
    def getDetails(self):
        #get the selected Index
        index=self.connection_list.currentRow()
        #get the connection according to the index
        connection=self.connectionPages[self.displayedIndex][index]
        #if stopList is empty request details
        if  connection.stopList==[]:
              #get reference link of connection
              urlString=connection.ref
              #request xml String
              xmlString=req.getXMLStringConnectionDetails(urlString)
              #check if valid
              if xmlString:
                    #remove all Elements from details QTableWidget
                    self.connection_details.setRowCount(0)
                    stopList=parser.getStopListFromXMLString(xmlString)
                    if not stopList=="":
                        #set the stopList of the connection to the local list
                        connection.addStopList(stopList)
                        #for every stop in stopList add it to QTableWidget
                        for s in connection.stopList:
                                self.addStopToDetails(s)
                        #set details_label text to connection information
                        self.details_label.setText(connection.toStringDetails())
                        #resize QTableWidget to contents
                        self.displayedIndexDetails=(self.displayedIndex,index)
                    else:
                        self.details_label.setText(self.errorMsg)        

    #previous navigation
    def showPreviousPage(self):
        #on first page do nothing
        #else go one page back and display
        if self.displayedIndex>0:
              self.displayedIndex=self.displayedIndex-1
              #remove old elements from QTableWidget
              self.connection_list.setRowCount(0)
              #for every connection add connection display it
              for c in self.connectionPages[self.displayedIndex]:
                   self.addConnectionToTable(c)
              self.setConnectionLabel()          

    #next navigation
    def showNextPage(self):
        #on last page do nothing
        #else go one page forward and display
        if self.displayedIndex<len(self.connectionPages)-1:
              self.displayedIndex=self.displayedIndex+1
              #remove all elements from QTableWidget
              self.connection_list.setRowCount(0)
              #for every connection add connection display it
              for c in self.connectionPages[self.displayedIndex]:
                   self.addConnectionToTable(c)
              #resize columns to contens
              self.setConnectionLabel()

    #sets the connection label to string repr. of the first displayed connection
    def setConnectionLabel(self):
        self.connection_label.setText(self.connectionPages[self.displayedIndex][0].toStringGenerall())

    #adds a connection to QTableWidget
    def addConnectionToTable(self,con):
        #add new row to QTableWidget
        self.connection_list.insertRow(self.connection_list.rowCount())
        #select last row of QTableWidget
        row=self.connection_list.rowCount()-1
        #add name of connection
        self.connection_list.setItem(row,connection_name_Index,qw.QTableWidgetItem(con.name))
        #check if direction and origin are valid and add them
        #not that direction (departure) an origin (arrival) are exclusive only one can be set!
        if con.direction:
                self.connection_list.setItem(row,connection_to_Index,qw.QTableWidgetItem(con.direction))
                self.connection_list.setItem(row,connection_from_Index,qw.QTableWidgetItem(con.stopName))
        if con.origin:
                self.connection_list.setItem(row,connection_from_Index,qw.QTableWidgetItem(con.origin))
                self.connection_list.setItem(row,connection_to_Index,qw.QTableWidgetItem(con.stopName))
        #add time of connection
        self.connection_list.setItem(row,connection_time_Index,qw.QTableWidgetItem(con.timeToString()))
        #if track is set add track of connection
        if con.track:
                self.connection_list.setItem(row,connection_track_Index,qw.QTableWidgetItem(con.track))

    #adds a stop to QTableWidget details
    def addStopToDetails(self,stop):
        #insert new row in QTableWidget details
        self.connection_details.insertRow(self.connection_details.rowCount())
        #select last row of QTableWidget details
        row=self.connection_details.rowCount()-1
        #add stopName 
        self.connection_details.setItem(row,details_stop_Index,qw.QTableWidgetItem(stop.name))
        #check if times and track are valid and add them
        if stop.arrTime:
                self.connection_details.setItem(row,details_arr_Index,qw.QTableWidgetItem(stop.arrTimeToString()))
        if stop.depTime:
                self.connection_details.setItem(row,details_dep_Index,qw.QTableWidgetItem(stop.depTimeToString()))
        if stop.track:
                self.connection_details.setItem(row,details_track_Index,qw.QTableWidgetItem(stop.track))

    #retrieves list all all matching stations to input and displays them
    def getStations(self):
        loc=self.inp.text()
        #check for empty input
        if loc.strip():
             #create xml-object
             xmlString=req.getXMLStringStationRequest(loc)
             #xmlString might be empty if HTTP-Error occured
             if xmlString:
                  (newStations,newStationsId)=parser.getStationsFromXMLString(xmlString)
                  #if something was actually found replace everything
                  if len(newStations)>0:
                      self.stationId=[]
                      self.railStations.clear()
                      self.stationId=newStationsId
                      self.railStations.addItems(newStations)

    #Encapsulation for calling from Button
    def getConnectionsNow(self):
        self.getConnectionsFromInput(True)

    #Encapsulation for calling from Button
    def getConnectionsWithTime(self):
        self.getConnectionsFromInput(False)

    def getConnectionsEarlier(self):
        self.getConnectionsWithShiftedTime(-1)

    def getConnectionsLater(self):
        self.getConnectionsWithShiftedTime(1)

    def getConnectionsWithShiftedTime(self,shift):
        if self.displayedIndex>-1:
                print(shift)
                #To-Do retrieve time, date and id of first Connection in QTableWidget
                # and arrival or departure etc...
                # shift time and if needed date
                #request connections with exsisting method..

    #retrieves all Connections matching to the inputs and displays them
    #isnow=TRUE use system time 
    #isnow=FALSE use choosen time
    def getConnectionsFromInput(self,isnow):
        #get selected Index from ComboBox
        index=self.railStations.currentIndex()
        #check invalid Index
        if index<0:
            return
        #use System-Time
        if isnow:
            date=qc.QDate.currentDate()
            time=qc.QTime.currentTime()
        #use selected time from gui        
        else:
            time=self.time_chooser.time()
            date=self.date_chooser.selectedDate()
        #get id to selected station
        identifier=self.stationId[index]
        #arrival or departure checked
        if self.arriv.isChecked():
            isDeparture=False
        else:
            isDeparture=True
        self.getConnections(date,time,identifier,isDeparture)
        
    #date and time as QDate and QTime object!
    #request the connection from or to the train station with given id at date and time    
    def getConnections(self,date,time,identifier,isDeparture):
        #request    
        xmlString=req.getXMLStringConnectionRequest(date,time,identifier,isDeparture)
        if xmlString:
            connections=parser.getConnectionsFromXMLString(xmlString,isDeparture)
            self.connection_list.setRowCount(0)
            if not connections=="":
                #clear displayed list
                #check if something was actually found 
                if connections==[]:
                        #if not set index to last entry of pages so this page can never be reached again
                        self.displayedIndex=len(self.connectionPages)-1
                        #set connection label to error Message
                        self.connection_label.setText(self.errorMsg)
                else:
                        #for every connection add connection display it
                        for c in connections:
                                self.addConnectionToTable(c)
                        #Add list of connections to pages
                        self.connectionPages.append(connections)
                        #set index to last entry of pages
                        self.displayedIndex=len(self.connectionPages)-1
                        #set connection label
                        self.setConnectionLabel()
            else:
                self.connection_label.setText(self.errorMsg) 

if __name__=="__main__":
        app=qw.QApplication(sys.argv)
        formwidget=FormWidget()
        formwidget.move(start_x_pos,start_y_pos)
        formwidget.show()
        sys.exit(app.exec_())


import sys
import time as tm

#import qt-stuff
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

from Structs import Filter
from Structs import Connection
from Structs import Stop
from Structs import ConnectionsList
from Widgets import QConnectionTable
from Widgets import QDetailsTable
from Widgets import QMapWidget

#import class for requests
import Request as req
#import class for parsing xml-String
import XMLParser as parser

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
        self.errorMsg="Keine Information  vorhanden"
        self.stationId=[]
        self.conList=ConnectionsList()
        self.defaultMapSize=300
        self.mapSizeMin=300
        self.mapSizeMax=800
        self.minTimeOffset=1
        self.maxTimeOffset=24
        self.filterActive=True

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
        self.depart=qw.QRadioButton("Abfahrten")
        self.arriv=qw.QRadioButton("Ankünfte")
        #group RadioButtons
        radioButton_layout=qw.QHBoxLayout()
        radioButton_layout.addWidget(self.depart)
        radioButton_layout.addWidget(self.arriv)
        #make RadioButtons checkable and set departure to default checked
        self.depart.setCheckable(True)
        self.arriv.setCheckable(True)
        self.depart.setChecked(True)
        
        self.checkFilter=qw.QCheckBox(" Filter ")
        filterLayout=qw.QHBoxLayout()
        filterLayout.addWidget(self.checkFilter)
        self.checkICE=qw.QCheckBox(" ICE/TGV ")
        self.checkIC=qw.QCheckBox(" IC/EC ")
        self.checkOther=qw.QCheckBox(" other ")
        filterLayout.addWidget(self.checkICE)
        filterLayout.addWidget(self.checkIC)
        filterLayout.addWidget(self.checkOther)
        
        self.mapActive=qw.QCheckBox(" Karte ")
        mapLayout=qw.QHBoxLayout()
        mapLayout.addWidget(self.mapActive)
        val=qg.QIntValidator(self.mapSizeMin,self.mapSizeMax)
        self.mapWidth=qw.QLineEdit()
        self.mapHeight=qw.QLineEdit()
        self.mapWidth.setValidator(val)
        self.mapHeight.setValidator(val)
        mapLayout.addWidget(qw.QLabel(" Breite: "))
        mapLayout.addWidget(self.mapWidth)
        mapLayout.addWidget(qw.QLabel(" Höhe: "))
        mapLayout.addWidget(self.mapHeight)
                
        #create buttons for getting connections earlier/later and group them
        requestEarlierLater_layout=qw.QHBoxLayout()
        self.earlier=qw.QPushButton("Früher")
        self.later=qw.QPushButton("Später")
        self.later.clicked.connect(self.getConnectionsLater)
        self.earlier.clicked.connect(self.getConnectionsEarlier)
        self.offsetField=qw.QLineEdit("3")
        val=qg.QIntValidator(self.minTimeOffset,self.maxTimeOffset)
        self.offsetField.setValidator(val)
        self.offsetField.setMaximumWidth(50)
        label=qw.QLabel(" Stunden ")
        label.setMaximumWidth(60)
        requestEarlierLater_layout.addWidget(self.offsetField)
        requestEarlierLater_layout.addWidget(label)
        requestEarlierLater_layout.addWidget(self.earlier)
        requestEarlierLater_layout.addWidget(self.later)
        
        #add layouts and widgets to layout for left part
        box1.addLayout(input1_layout)
        box1.addLayout(input2_layout)
        box1.addWidget(self.date_chooser)
        box1.addLayout(radioButton_layout)
        box1.addLayout(filterLayout)
        box1.addLayout(mapLayout)
        box1.addLayout(requestEarlierLater_layout)
        box1.addLayout(request_layout)

        #layout for middle part of gui
        box2=qw.QVBoxLayout()

        #label for connectionTable
        self.connection_label=qw.QLabel("")
        #QTableWidget for displaying connections
        self.connectionTable=QConnectionTable()
        #connect connectionTable with function
        self.connectionTable.clicked.connect(self.getDetails)
        
        #button for navigating
        self.prev=qw.QPushButton("Vorherige")
        self.prev.clicked.connect(self.showPreviousPage)
        #button for refreshing the page using new filter
        self.reload=qw.QPushButton("Aktualisieren")
        self.reload.clicked.connect(self.refreshPage)
        #button for navigating
        self.next=qw.QPushButton("Nächste")
        self.next.clicked.connect(self.showNextPage)

        #layout for connectionTable navigation
        navigation_layout=qw.QHBoxLayout()
        #add buttons to navigation layout        
        navigation_layout.addWidget(self.prev)
        navigation_layout.addWidget(self.reload)
        navigation_layout.addWidget(self.next)
         
        #add widgets and layouts to layout for middle part
        box2.addWidget(self.connection_label)
        box2.addWidget(self.connectionTable)
        box2.addLayout(navigation_layout)
        
        #layout for right part of gui
        box3=qw.QVBoxLayout()
        
        #label for details of a connection
        self.details_label=qw.QLabel("")
        #QTableWidget for presenting detailed data of a connection
        self.detailsTable=QDetailsTable()
        #connect QTableWidget with function
        self.detailsTable.clicked.connect(self.getConnectionsOnClickInDetails)
                
        #add label to box3
        box3.addWidget(self.details_label)
        #add QTableWidget to box3
        box3.addWidget(self.detailsTable)
 
        #add all layouts to form-Layout
        layout.addLayout(box1)
        layout.addLayout(box2)
        layout.addLayout(box3)
        
        #set formLayout
        self.setLayout(layout)
        
        #initalize Widget for map
        self.mapWidget=QMapWidget()
        
    #called on click of detailsTable
    def getConnectionsOnClickInDetails(self):
        #get selected Row in connection details
        row=self.detailsTable.currentRow()
        #get the displayedIndex Information
        (pageIndex,connectionIndexOnPage)=self.conList.getDetailsIndices()
        #select the clicked stop from the displayed Connection (Details)
        s=self.conList.getStop(pageIndex,connectionIndexOnPage,row)
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
        
    #called on click of connectionTable
    #request connection details if needed and displays them  
    def getDetails(self):
        #get the selected Index
        index=self.connectionTable.currentRow()
        #get the connection according to the index
        connection=self.conList.getSingleConnection(self.conList.getDisplayedIndex(),index)
        #if stopList is empty request details information
        if  connection.stopList==[]:
              #get reference link of connection
              urlString=connection.ref
              #request xml String
              xmlString=req.getXMLStringConnectionDetails(urlString)
              #check if valid
              if xmlString:
                    #remove all Elements from details QTableWidget
                    self.detailsTable.setRowCount(0)
                    stopList=parser.getStopListFromXMLString(xmlString)
                    if not stopList=="":
                        #set the stopList of the connection to the local list
                        connection.stopList=stopList
                    else:
                        self.details_label.setText(self.errorMsg)
                        return
        #for every stop in stopList add it to QTableWidget
        coordinates=[]
        for i in range(0,len(connection.stopList)):
                self.addStopToDetails(connection.stopList[i])
                coordinates.append(connection.stopList[i].pos)
                if connection.stopList[i].id==connection.stopid:
                        markerIndex=i
        #set details_label text to connection information
        self.details_label.setText(connection.toStringDetails())
        self.conList.setDisplayedDetailedIndex(self.conList.getDisplayedIndex(),index)

        #check if imageData is empty and if map is selected   
        if connection.imageData.isEmpty() and self.mapActive.isChecked():
                #try to convert desired height and with to int
                try:
                        height=int(self.mapHeight.text())
                        width=int(self.mapWidth.text())
                #on error use default values               
                except ValueError:
                        height=self.defaultMapSize
                        width=self.defaultMapSize
                #size to small use default size
                if height<self.defaultMapSize or width<self.defaultMapSize:
                        height=self.defaultMapSize
                        width=self.defaultMapSize
                #request imageData and create QByteArray and set imageData
                connection.imageData=qc.QByteArray(req.getMapWithLocations(coordinates,markerIndex,width,height))
        #display requested map-Data
        if self.mapActive.isChecked():
                self.mapWidget.showMap(connection.imageData,connection.toStringDetails())

    #previous navigation
    def showPreviousPage(self):
        #on first page do nothing
        #else go one page back and display
        if self.conList.getDisplayedIndex()>0:
              self.conList.setDisplayedIndex(self.conList.getDisplayedIndex()-1)
              #remove old elements from QTableWidget
              self.connectionTable.setRowCount(0)
              #for every connection add connection display it
              self.addConnections(self.conList.getConnectionPage(self.conList.getDisplayedIndex()))
              self.setConnectionLabel()      

    def refreshPage(self):
        self.connectionTable.setRowCount(0)
        self.addConnections(self.conList.getConnectionPage(self.conList.getDisplayedIndex()))
        
    #next navigation
    def showNextPage(self):
        #on last page do nothing
        #else go one page forward and display
        if self.conList.getDisplayedIndex()<self.conList.getPageCount()-1:
              self.conList.setDisplayedIndex(self.conList.getDisplayedIndex()+1)
              #remove all elements from QTableWidget
              self.connectionTable.setRowCount(0)
              #for every connection add connection display it
              self.addConnections(self.conList.getConnectionPage(self.conList.getDisplayedIndex()))
              #resize columns to contens
              self.setConnectionLabel()

    def addConnections(self,connections):
        self.filterActive=self.checkFilter.isChecked()
        ICE=self.checkICE.isChecked()
        IC=self.checkIC.isChecked()
        Other=self.checkOther.isChecked()
        #minimum one filter type must be selected
        if ICE or IC or Other:
                self.typeFilter=Filter(ICE,IC,Other)
        else:
                self.filterActive=False
        #add all connections to table
        for c in connections:
              self.addConnectionToTable(c)
        #displayed connections shall be filtered
        if self.filterActive:
                #all Indices of original connections that shall be displayed
                displayIndex=self.typeFilter.filter(connections)
                #for each index in the list
                for ind in displayIndex:
                        #display corresponding row
                        self.connectionTable.setRowHidden(ind,False)

    #sets the connection label to string repr. of the first displayed connection
    def setConnectionLabel(self):
        self.connection_label.setText(self.conList.getSingleConnection(self.conList.getDisplayedIndex(),0).toStringGenerall())

    #adds a connection to QTableWidget
    def addConnectionToTable(self,con):
        #add new row to QTableWidget
        self.connectionTable.insertRow(self.connectionTable.rowCount())
        #select last row of QTableWidget
        row=self.connectionTable.rowCount()-1
        #for active filter hide everything on default 
        if self.filterActive:
                self.connectionTable.setRowHidden(row,True)
        #add name of connection
        self.connectionTable.setItem(row,QConnectionTable.name_Index,qw.QTableWidgetItem(con.name))
        #check if direction and origin are valid and add them
        #not that direction (departure) an origin (arrival) are exclusive only one can be set!
        if con.direction:
                self.connectionTable.setItem(row,QConnectionTable.to_Index,qw.QTableWidgetItem(con.direction))
                self.connectionTable.setItem(row,QConnectionTable.from_Index,qw.QTableWidgetItem(con.stopName))
        if con.origin:
                self.connectionTable.setItem(row,QConnectionTable.from_Index,qw.QTableWidgetItem(con.origin))
                self.connectionTable.setItem(row,QConnectionTable.to_Index,qw.QTableWidgetItem(con.stopName))
        #add time of connection
        self.connectionTable.setItem(row,QConnectionTable.time_Index,qw.QTableWidgetItem(con.timeToString()))
        #if track is set add track of connection
        if con.track:
                self.connectionTable.setItem(row,QConnectionTable.track_Index,qw.QTableWidgetItem(con.track))

    #adds a stop to QTableWidget details
    def addStopToDetails(self,stop):
        #insert new row in QTableWidget details
        self.detailsTable.insertRow(self.detailsTable.rowCount())
        #select last row of QTableWidget details
        row=self.detailsTable.rowCount()-1
        #add stopName 
        self.detailsTable.setItem(row,QDetailsTable.stop_Index,qw.QTableWidgetItem(stop.name))
        #check if times and track are valid and add them
        if stop.arrTime:
                self.detailsTable.setItem(row,QDetailsTable.arr_Index,qw.QTableWidgetItem(stop.arrTimeToString()))
        if stop.depTime:
                self.detailsTable.setItem(row,QDetailsTable.dep_Index,qw.QTableWidgetItem(stop.depTimeToString()))
        if stop.track:
                self.detailsTable.setItem(row,QDetailsTable.track_Index,qw.QTableWidgetItem(stop.track))

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

    #ealier means subtract hours
    def getConnectionsEarlier(self):
        try:
                hourShift=int(self.offsetField.text())
        except ValueError:
                return
        self.getConnectionsWithShiftedTime(-1,hourShift)

    #later means add hours
    def getConnectionsLater(self):
        try:
                hourShift=int(self.offsetField.text())
        except ValueError:
                return
        self.getConnectionsWithShiftedTime(1,hourShift)

    #
    def getConnectionsWithShiftedTime(self,shift,numbersOfHoursShifted=3):
        #something has to be displayed at the moment or nothing can be read from table
        if self.conList.getDisplayedIndex()>-1:
                #get the first connection
                con=self.conList.getSingleConnection(self.conList.getDisplayedIndex(),0)
                #get id, date and time
                identifier=con.stopid
                date=con.date
                time=con.time
                # direction is not set means it is a arrival
                if con.direction=="":
                        isDeparture=False
                # origin is not set so it is a departure
                if con.origin=="":
                        isDeparture=True
                #add shift to requested time
                newTime=time.addSecs(shift*3600*numbersOfHoursShifted)
                #added hours but new Time less than before -> day overflow, thus add one day
                if newTime < time and shift>0:
                        date=date.addDays(1)
                #subtracted hours but new Time greater than before -> day underflow, thus subtract one day
                if newTime > time and shift<0:
                        date=date.addDays(-1)
                #request new connections
                self.getConnections(date,newTime,identifier,isDeparture)

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
            self.connectionTable.setRowCount(0)
            if not connections=="":
                #clear displayed list
                #check if something was actually found 
                if connections==[]:
                        #if not set index to last entry of pages so this page can never be reached again
                        self.conList.setDisplayedIndex(self.conList.getPageCount()-1)
                        #set connection label to error Message
                        self.connection_label.setText(self.errorMsg)
                else:
                        self.addConnections(connections)
                        #Add list of connections to pages
                        self.conList.appendPage(connections)
                        #set index to last entry of pages
                        self.conList.setDisplayedIndex(self.conList.getPageCount()-1)
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


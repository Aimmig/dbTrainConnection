import sys
import time as tm

#import qt-stuff
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

from Connection import Connection
from Stop import Stop

#import xml stuff
import xml.etree.ElementTree as ET
#import class for requests
import Request as req

#converts String formatted as hh:mm to QTime object
def timeStringToQTime(timeString):
     splittedTime=timeString.split(":")
     hours=int(splittedTime[0])
     minutes=int(splittedTime[1])
     time=qc.QTime(hours,minutes)
     return time
    
#converts String formatted as yyyy-mm-dd to QDate object
def dateStringToQDate(dateString):
     splittedDate=dateString.split("-")
     year=int(splittedDate[0])
     month=int(splittedDate[1])
     day=int(splittedDate[2])
     date=qc.QDate(year,month,day)
     return date

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

        #add layouts and widgets to layout for left part
        box1.addLayout(input1_layout)
        box1.addLayout(input2_layout)
        box1.addWidget(self.date_chooser)
        box1.addLayout(radioButton_layout)
        box1.addLayout(request_layout)

        #layout for middle part of gui
        box2=qw.QVBoxLayout()

        #label for connection list
        self.connection_label=qw.QLabel("")
        self.connection_label.setSizePolicy(qw.QSizePolicy.Preferred,qw.QSizePolicy.Fixed)
        #QTableWidget for displaying connections
        self.connection_list=qw.QTableWidget()
        #use 5 columns to present data
        self.connection_list.setColumnCount(5)
        self.connection_list.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
        #set Horizontal Header for QTableWidget
        header_list=["Zugnummer","von","nach","Uhrzeit","Gleis"]
        self.connection_list.setHorizontalHeaderLabels(header_list)
        #set minimal sizes for every column
        #self.connection_list.setColumnWidth(0,100)
        #self.connection_list.setColumnWidth(1,120)
        #self.connection_list.setColumnWidth(2,100)
        #self.connection_list.setColumnWidth(3,80)
        #self.connection_list.setColumnWidth(4,80)
        #self.connection_list.setMinimumSize(80+300+40,100)
        #do not show grind and vertical Headers
        self.connection_list.setShowGrid(False)
        self.connection_list.verticalHeader().setVisible(False)
        self.connection_list.setSizePolicy(qw.QSizePolicy.Preferred,qw.QSizePolicy.Ignored)
        #set Horizontal Resize mode to interactive
        self.connection_list.horizontalHeader().setSectionResizeMode(qw.QHeaderView.Interactive)
        self.connection_list.resizeColumnsToContents()
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
        self.details_label.setSizePolicy(qw.QSizePolicy.Preferred,qw.QSizePolicy.Fixed)
        #QTableWidget for presenting detailed data of a connection
        self.connection_details=qw.QTableWidget()
        self.connection_details.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
        #use for columns to present data
        self.connection_details.setColumnCount(4)
        self.connection_details.setSizePolicy(qw.QSizePolicy.Preferred,qw.QSizePolicy.Ignored)
        #set Horizontal Headers for QTableWidget
        header_details_list=["Halt","Ankunft","Abfahrt","Gleis"]
        self.connection_details.setHorizontalHeaderLabels(header_details_list)
        #set minimal sizes of ever Column
        #self.connection_details.setColumnWidth(0,150)
        #self.connection_details.setColumnWidth(1,80)
        #self.connection_details.setMinimumSize(450,100)
        #do not show grid
        self.connection_details.setShowGrid(False)
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
                    #create xml object from string
                    root=ET.fromstring(xmlString)
                    stopList=[]
                    for c in root:
                        if c.tag=="Stops":
                              #iterate over all Stops
                              for child in c:        
                                  #name and id of the station are mandatory         
                                  name=child.attrib['name']
                                  identifier=child.attrib['id']
                                  #departure and arrive time and date might not be set
                                  # convert all times and dates to QDate and QTime objects
                                  if 'arrTime' in child.attrib:
                                      arrTimeString=child.attrib['arrTime']
                                      arrTime=timeStringToQTime(arrTimeString)
                                  else:
                                      arrTime=""
                                  if 'arrDate' in child.attrib:
                                      arrDateString=child.attrib['arrDate']
                                      arrDate=dateStringToQDate(arrDateString)
                                  else:
                                      arrDate=""
                                  if 'depTime' in child.attrib:
                                      depTimeString=child.attrib['depTime']
                                      depTime=timeStringToQTime(depTimeString)
                                  else:
                                      depTime=""
                                  if 'depDate' in child.attrib:
                                      depDateString=child.attrib['depDate']
                                      depDate=dateStringToQDate(depDateString)
                                  else:
                                      depDate=""
                                  #track might not be set
                                  if 'track' in child.attrib:
                                      track=child.attrib['track']
                                  else:
                                      track=""
                                  #longitude, latitude are mandatory
                                  lon=child.attrib['lon']
                                  lat=child.attrib['lat']
                                  #create stop with all these informations
                                  stop=Stop(name,identifier,arrTime,arrDate,depTime,depDate,track,lon,lat)
                                  #add it to local list
                                  stopList.append(stop)
                    #set the stopList of the connection to the local list
                    connection.addStopList(stopList)
        #remove all Elements from details QTableWidget
        self.connection_details.setRowCount(0)
        #for every stop in stopList add it to QTableWidget
        for s in connection.stopList:
             self.addStopToDetails(s)
        #set details_label text to connection information
        self.details_label.setText(connection.toStringDetails())
        #resize QTableWidget to contents
        self.connection_details.resizeColumnsToContents()
        self.displayedIndexDetails=(self.displayedIndex,index)

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
              #resize colums to contens
              self.connection_list.resizeColumnsToContents()
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
              self.connection_list.resizeColumnsToContents()
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
        self.connection_list.setItem(row,0,qw.QTableWidgetItem(con.name))
        #check if direction and origin are valid and add them
        #not that direction (departure) an origin (arrival) are exclusive only one can be set!
        if con.direction:
                self.connection_list.setItem(row,2,qw.QTableWidgetItem(con.direction))
                self.connection_list.setItem(row,1,qw.QTableWidgetItem(con.stopName))
        if con.origin:
                self.connection_list.setItem(row,1,qw.QTableWidgetItem(con.origin))
                self.connection_list.setItem(row,2,qw.QTableWidgetItem(con.stopName))
        #add time of connection
        self.connection_list.setItem(row,3,qw.QTableWidgetItem(con.timeToString()))
        #if track is set add track of connection
        if con.track:
                self.connection_list.setItem(row,4,qw.QTableWidgetItem(con.track))

    #adds a stop to QTableWidget details
    def addStopToDetails(self,stop):
        #insert new row in QTableWidget details
        self.connection_details.insertRow(self.connection_details.rowCount())
        #select last row of QTableWidget details
        row=self.connection_details.rowCount()-1
        #add stopName 
        self.connection_details.setItem(row,0,qw.QTableWidgetItem(stop.name))
        #check if times and track are valid and add them
        if stop.arrTime:
                self.connection_details.setItem(row,1,qw.QTableWidgetItem(stop.arrTimeToString()))
        if stop.depTime:
                self.connection_details.setItem(row,2,qw.QTableWidgetItem(stop.depTimeToString()))
        if stop.track:
                self.connection_details.setItem(row,3,qw.QTableWidgetItem(stop.track))

    #retrieves list all all matching stations to input and displays them
    def getStations(self):
        loc=self.inp.text()
        #check for empty input
        if loc.strip():
             #create xml-object
             xmlString=req.getXMLStringStationRequest(loc)
             #xmlString might be empty if HTTP-Error occured
             if xmlString:
                  root=ET.fromstring(xmlString)
                  #write id and names to temporary variable
                  newStationsId=[]
                  newStations=[]
                  #iterate over all childs and add attributes to lists
                  for child in root:
                      newStationsId.append(child.attrib['id'])
                      newStations.append(child.attrib['name'])
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
            root=ET.fromstring(xmlString)
            #iterate over all connections
            connections=[]
            for con in root:
                   #connection name is mandatory
                   name=con.attrib['name']
                   # check if type exist --spelling mistake in xml
                   if 'type' in con.attrib:
                       typ=con.attrib['type']
                   else:
                       typ=""
                   #stop, id and time, date are mandatory
                   stopid=con.attrib['stopid']
                   stopName=con.attrib['stop']
                   #convert time and date string to Qt Objects
                   timeString=con.attrib['time']
                   time=timeStringToQTime(timeString)
                   dateString=con.attrib['date']
                   date=dateStringToQDate(dateString)
                   #read direction if departure
                   if isDeparture and 'direction' in con.attrib:
                       direction=con.attrib['direction']
                       origin=""
                   elif not isDeparture and 'origin' in con.attrib:
                       origin=con.attrib['origin']
                       direction=""
                   else:
                        origin=""
                        direction=""
                   #track might not be set in xml
                   if 'track' in con.attrib:
                       track=con.attrib['track']
                   else:
                       track=""
                   #read reference link
                   for details in con :
                       if 'ref' in details.attrib:
                           ref=details.attrib['ref']
                       else:
                           ref=""
                   #add connection with these information to local list of connections
                   connections.append(Connection(name,typ,stopid,stopName,time,date,direction,origin,track,ref))
            #clear displayed list
            self.connection_list.setRowCount(0)
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
                #resize columns to contents
                self.connection_list.resizeColumnsToContents()
                #Add list of connections to pages
                self.connectionPages.append(connections)
                #set index to last entry of pages
                self.displayedIndex=len(self.connectionPages)-1
                #set connection label
                self.setConnectionLabel()

if __name__=="__main__":
        app=qw.QApplication(sys.argv)
        formwidget=FormWidget()
        formwidget.show()
        sys.exit(app.exec_())


import sys
import time as tm

#import qt-stuff
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

#import xml stuff
import xml.etree.ElementTree as ET
#import class for requests
import Request as req

class Connection:
        
    def __init__(self,name,typ,stopid,stopName,time,date,direction,origin,track,ref):
        self.name=name
        self.type=typ
        self.stopid=stopid
        self.stopName=stopName
        self.time=time
        self.date=date
        self.direction=direction
        self.origin=origin
        self.track=track
        self.ref=ref
        self.stopList=[]

    def addStopList(self,l):
        self.stopList=l

class Stop:

    def __init__(self,name,identifier,arrTime,arrDate,depTime,depDate,track,lon,lat):
        self.name=name
        self.id=identifier
        self.arrTime=arrTime
        self.arrDate=arrDate
        self.depTime=depTime
        self.depDate=depDate
        self.track=track
        self.lon=lon
        self.lat=lat;

    def toString(self):
        res=self.name+" "+self.track+" "+self.depTime+" "+self.depDate
        return res

#Class that defines gui
class FormWidget(qw.QWidget):

    #constructor for gui
    def __init__(self):

        #super constructor
        super(FormWidget,self).__init__()
        
        #set some properties
        self.setAutoFillBackground(True)
        self.setWindowTitle("Fahrplanzeige")
        self.stationId=[]
        self.connectionPages=[]
        self.displayedIndex=-1

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
        #list for all connections
        self.connection_list=qw.QTableWidget()
        self.connection_list.setColumnCount(5)
        self.header_list=["Zugnummer","von","nach","Uhrzeit","Gleis"]
        self.connection_list.setHorizontalHeaderLabels(self.header_list)
        self.connection_list.setMinimumSize(600,100)
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
        
        box3=qw.QVBoxLayout()
        
        self.details_label=qw.QLabel("Details")
        self.connection_details=qw.QTableWidget()
        self.connection_details.setColumnCount(6)
        self.connection_details.setMinimumSize(450,100)
        self.header_details_list=["Halt","AnkunftsZeit","Ankunftsdatum","Abfahrtszeit","Abfahrtsdatum","Gleis"]
        self.connection_details.setHorizontalHeaderLabels(self.header_details_list)
        box3.addWidget(self.details_label)
        box3.addWidget(self.connection_details)
 
        #add all layouts to form-Layout
        layout.addLayout(box1)
        layout.addLayout(box2)
        layout.addLayout(box3)
        
        #set formLayout
        self.setLayout(layout)
        
    def getDetails(self):
        index=self.connection_list.currentRow()
        if  self.connectionPages[self.displayedIndex][index].stopList==[]:
              urlString=self.connectionPages[self.displayedIndex][index].ref
              xmlString=req.getXMLStringConnectionDetails(urlString)
              if xmlString:
                    root=ET.fromstring(xmlString)
                    stopList=[]
                    for c in root:
                        if c.tag=="Stops":
                              for child in c:                  
                                  name=child.attrib['name']
                                  identifier=child.attrib['id']
                                  if 'arrTime' in child.attrib:
                                      arrTime=child.attrib['arrTime']
                                  else:
                                      arrTime=""
                                  if 'arrDate' in child.attrib:
                                      arrDate=child.attrib['arrDate']
                                  else:
                                      arrDate=""
                                  if 'depTime' in child.attrib:
                                      depTime=child.attrib['depTime']
                                  else:
                                      depTime=""
                                  if 'depDate' in child.attrib:
                                      depDate=child.attrib['depDate']
                                  else:
                                      depDate=""
                                  if 'track' in child.attrib:
                                      track=child.attrib['track']
                                  else:
                                      track=""
                                  lon=child.attrib['lon']
                                  lat=child.attrib['lat']
                                  stop=Stop(name,identifier,arrTime,arrDate,depTime,depDate,track,lon,lat)
                                  stopList.append(stop)
                    self.connectionPages[self.displayedIndex][index].addStopList(stopList)
        self.connection_details.setRowCount(0)
        self.connection_details.setHorizontalHeaderLabels(self.header_details_list)
        for s in self.connectionPages[self.displayedIndex][index].stopList:
             self.addStopToDetails(s)

    #previous navigation
    def showPreviousPage(self):
        #on first page do nothing
        #else go one page back and display
        if self.displayedIndex>0:
              self.displayedIndex=self.displayedIndex-1
              self.connection_list.setRowCount(0)
              #for every connection add connection display it
              for c in self.connectionPages[self.displayedIndex]:
                   self.addConnectionToTable(c)            

    #next navigation
    def showNextPage(self):
        #on last page do nothing
        #else go one page forward and display
        if self.displayedIndex<len(self.connectionPages)-1:
              self.displayedIndex=self.displayedIndex+1
              self.connection_list.setRowCount(0)
              #for every connection add connection display it
              for c in self.connectionPages[self.displayedIndex]:
                   self.addConnectionToTable(c)

    def addConnectionToTable(self,con):
        labelString="Fahrplantabelle für "+con.stopName+" am "+con.date
        self.connection_label.setText(labelString)
        self.connection_list.insertRow(self.connection_list.rowCount())
        column=self.connection_list.rowCount()-1
        self.connection_list.setItem(column,0,qw.QTableWidgetItem(con.name))
        if con.direction:
                self.connection_list.setItem(column,2,qw.QTableWidgetItem(con.direction))
                self.connection_list.setItem(column,1,qw.QTableWidgetItem(con.stopName))
        if con.origin:
                self.connection_list.setItem(column,1,qw.QTableWidgetItem(con.origin))
                self.connection_list.setItem(column,2,qw.QTableWidgetItem(con.stopName))
        self.connection_list.setItem(column,3,qw.QTableWidgetItem(con.time))
        if con.track:
                self.connection_list.setItem(column,4,qw.QTableWidgetItem(con.track))

    def addStopToDetails(self,stop):
        labelString="Zugverlauf "
        self.connection_label.setText(labelString)
        self.connection_details.insertRow(self.connection_details.rowCount())
        column=self.connection_details.rowCount()-1
        self.connection_details.setItem(column,0,qw.QTableWidgetItem(stop.name))
        if stop.arrTime:
                self.connection_details.setItem(column,1,qw.QTableWidgetItem(stop.arrTime))
        if stop.arrDate:
                self.connection_details.setItem(column,2,qw.QTableWidgetItem(stop.arrDate))
        if stop.depDate:
                self.connection_details.setItem(column,3,qw.QTableWidgetItem(stop.depDate))
        if stop.depTime:
                self.connection_details.setItem(column,4,qw.QTableWidgetItem(stop.depTime))
        if stop.track:
                self.connection_details.setItem(column,5,qw.QTableWidgetItem(stop.track))

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
        return

    #Encapsulation for calling from Button
    def getConnectionsNow(self):
        self.getConnections(True)

    #Encapsulation for calling from Button
    def getConnectionsWithTime(self):
        self.getConnections(False)

    #retrieves all Connections matching to the inputs and displays them
    #isnow=TRUE use system time 
    #isnow=FALSE use choosen time
    def getConnections(self,isnow):
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
        #request    
        xmlString=req.getXMLStringConnectionRequest(date,time,identifier,isDeparture)
        if xmlString:
            root=ET.fromstring(xmlString)
            #iterate over all connections
            connections=[]
            for con in root:
                   name=con.attrib['name']
                   # check if type exist --spelling mistake in xml
                   if 'type' in con.attrib:
                       typ=con.attrib['type']
                   else:
                       typ=""
                   stopid=con.attrib['stopid']
                   stopName=con.attrib['stop']
                   time=con.attrib['time']
                   date=con.attrib['date']
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
                   connections.append(Connection(name,typ,stopid,stopName,time,date,direction,origin,track,ref))
            #clear displayed list
            self.connection_list.setRowCount(0)
            #for every connection add connection display it
            for c in connections:
                   self.addConnectionToTable(c)
            #Add list of connections to pages
            self.connectionPages.append(connections)
            #set index to last entry of pages
            self.displayedIndex=len(self.connectionPages)-1
                     
if __name__=="__main__":
        app=qw.QApplication(sys.argv)
        formwidget=FormWidget()
        formwidget.show()
        sys.exit(app.exec_())


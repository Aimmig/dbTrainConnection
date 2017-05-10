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
        
    def __init__(self,name,typ,stopid,stopName,time,date,direction,track,ref):
        self.name=name
        self.type=typ
        self.stopid=stopid
        self.stopName=stopName
        self.time=time
        self.date=date
        self.direction=direction
        self.track=track
        self.ref=ref
        self.stopList=[]

    def addStopList(self,l):
        self.stopList=l    

    def toString(self):
        res=self.name+" "+self.stopName
        res=res+" "+self.time+" "+self.direction+" "+self.track
        return res

class Stop:

    def __init__self(self,name,identifier,arrTime,arrDate,depTime,depDate,track,lon,lat):
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
        return self.name+" "+self.depTime

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
        #self.date_chooser.gridVisible(True)

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
        self.connection_label=qw.QLabel("Fahrplantabelle")
        #list for all connections
        self.connection_list=qw.QListWidget()
        self.connection_list.setMinimumSize(450,100)
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
        self.connection_details=qw.QListWidget()
        self.connection_details.setMinimumSize(450,100)
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
        urlString=self.connectionPages[self.displayedIndex][index].ref
        print(urlString)
        xmlString=req.getXMLStringConnectionDetails(urlString)
        if xmlString and self.connectionPages[self.displayedIndex][index].stopList==[]:
              root=ET.fromstring(xmlString)
              stopList=[]
              #TO-DO: Iterate corectly over xml- object !!!
              for 'Stop' in root.attrib['Stops']:
                        name=root.attrib['Stops'].attrib['name']
                        print(name)
                        identifier=child.attrib['id']
                        arrTime=child.attrib['arrTime']
                        arrDate=child.attrib['arrDate']
                        depTime=child.attrib['depTime']
                        depDate=child.attrib['depDate']
                        track=child.attrib['track']
                        lon=child.attrib['lon']
                        lat=child.attrib['lat']
                        stop=Stop(name,identifier,arrTime,arrDate,depTime,depDate,track,lon,lat)
                        stopList.append(Stop)
                        print(name)
              self.connectionPages[self.displayedIndex][index].addStopList(stopList)
        self.connection_details.clear()
        for s in self.connectionPages[self.displayedIndex][index].stopList:
              print(s.toString())

    #previous navigation
    def showPreviousPage(self):
        #on first page do nothing
        #else go one page back and display
        if self.displayedIndex>0:
              self.displayedIndex=self.displayedIndex-1
              self.connection_list.clear()
              for k in self.connectionPages[self.displayedIndex]:
                    self.connection_list.addItem(k.toString())                

    #next navigation
    def showNextPage(self):
        #on last page do nothing
        #else go one page forward and display
        if self.displayedIndex<len(self.connectionPages)-1:
              self.displayedIndex=self.displayedIndex+1
              self.connection_list.clear()
              for k in self.connectionPages[self.displayedIndex]:
                    self.connection_list.addItem(k.toString())               

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
            date=self.date_chooser.selectedDate()
            time=self.time_chooser.time()
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
                   if isDeparture:
                       direction=con.attrib['direction']
                   else:
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
                   connections.append(Connection(name,typ,stopid,stopName,time,date,direction,track,ref))
            #clear displayed list
            self.connection_list.clear()
            #for every connection add connection display it
            for k in connections:
                self.connection_list.addItem(k.toString())
            #Add list of connections to pages
            self.connectionPages.append(connections)
            #set index to last entry of pages
            self.displayedIndex=len(self.connectionPages)-1
                     
if __name__=="__main__":
        app=qw.QApplication(sys.argv)
        formwidget=FormWidget()
        formwidget.show()
        sys.exit(app.exec_())


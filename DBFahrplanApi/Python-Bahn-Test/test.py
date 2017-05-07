import sys
import time as tm
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

import urllib.request as url_req
import xml.etree.ElementTree as ET

KEY="DBhackFrankfurt0316"
LANGUAGE="de"
BASE_URL="https://open-api.bahn.de/bin/rest.exe/"

class FormWidget(qw.QWidget):

    def __init__(self):
        #super constructor
        super(FormWidget,self).__init__()
        
        #set some properties
        self.setAutoFillBackground(True)
        self.setWindowTitle("Fahrplanzeige")
        self.StationList=[]

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

        #add layouts and widgets to layout for left part
        box1.addLayout(input1_layout)
        box1.addLayout(input2_layout)
        box1.addWidget(self.date_chooser)
        box1.addLayout(request_layout)

        #layout for middle part of gui
        box2=qw.QVBoxLayout()

        #label for connection list
        self.connection_label=qw.QLabel("Fahrplantabelle")
        #list for all connections
        self.connection_list=qw.QListWidget()
        #button for navigating
        self.prev=qw.QPushButton("Vorherige")
        #button for navigating
        self.next=qw.QPushButton("Nächste")

        #layout for connection_list navigation
        navigation_layout=qw.QHBoxLayout()
        #add buttons to navigation layout        
        navigation_layout.addWidget(self.prev)
        navigation_layout.addWidget(self.next)
         
        #add widgets and layouts to layout for middle part
        box2.addWidget(self.connection_label)
        box2.addWidget(self.connection_list)
        box2.addLayout(navigation_layout)
        
        #add all layouts to form-Layout
        layout.addLayout(box1)
        layout.addLayout(box2)
        
        #set formLayout
        self.setLayout(layout)

    #retrieves list all all matching stations to input and displays them
    def getStations(self):
        loc=self.inp.text()
        root=ET.fromstring(getXMLStringStationRequest(loc))
        self.StationList=[]
        self.railStations.clear()
        for child in root:
            self.StationList.append(child.attrib['id'])
            self.railStations.addItem(child.attrib['name'])

    def getConnectionsNow(self):
        self.getConnections(True)

    def getConnectionsWithTime(self):
        self.getConnections(False)

    #retrieves all Connections matching to the inputs and displays them
    #isnow=TRUE use system time 
    #isnow=FALSE use choosen time
    def getConnections(self,isnow):
        if isnow:
            date=qc.QDate.currentDate()
            time=qc.QTime.currentTime()          
        else:
            date=self.date_chooser.selectedDate()
            time=self.time_chooser.time()
        index=self.railStations.currentIndex()
        identifier=self.StationList[index]
        if index<0:
            return
        else:
            print(getXMLStringConnectionRequest(date,time,identifier,True))

#returns the XML-String representation of the requested ressource
def getXMLStringStationRequest(loc):
        url=createStationRequestURL(loc)
        req=url_req.Request(url)
        try:
            with url_req.urlopen(req) as response:
                result=response.read()
                return result
        except HTTPError as e:
             print('The server couldn\'t fulfill the request.')
             print('Error code: ', e.code)
        except URLError as e:
             print('We failed to reach a server.')
             print('Reason: ', e.reason)
        return ""

def getXMLStringConnectionRequest(date,time,identifier,isDeparture):
        url=createConnectionRequestURL(date,time,identifier,isDeparture)
        req=url_req.Request(url)
        try:
            with url_req.urlopen(req) as response:
                result=response.read()
                return result
        except HTTPError as e:
             print('The server couldn\'t fulfill the request.')
             print('Error code: ', e.code)
        except URLError as e:
             print('We failed to reach a server.')
             print('Reason: ', e.reason)
        return ""

#creates the URL for requesting Connections
def createConnectionRequestURL(date,time,identifier,isDeparture):
        #build date-String
        dateString=str(date.year())+"-"+str(date.month())+"-"+str(date.day())
        #build and encode timeString
        timeString=str(time.hour())+"%3A"+str(time.minute())
        lastPart=KEY+"&lang="+LANGUAGE+"&id="+str(identifier)+"&date="+dateString+"&time"+timeString
        if isDeparture:
             return BASE_URL+"departureBoard?authKey="+lastPart
        else:
             return BASE_URL+"arrivalBoard?authKey="+lastPart

#creates the URL for requesting Stations
def createStationRequestURL(loc):
        return BASE_URL+"location.name?authKey="+KEY+"&lang="+LANGUAGE+"&input="+loc 

if __name__=="__main__":
        app=qw.QApplication(sys.argv)
        formwidget=FormWidget()
        formwidget.show()
        sys.exit(app.exec_())


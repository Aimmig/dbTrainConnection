#    -----------------------------------------------------------------------
#    This programm requests connections and corresponding details from the
#    API of Deutsche Bahn and presents them in an user interface.
#    This file encapsulates the main gui, handels the gui navigation and
#    defines logic to display the information.
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
from Request import Request as req
from SettingsWidget import SettingsWidget
import XMLParser as parser
import sys
import urllib.error as err

#Class that defines gui
class FormWidget(qw.QWidget):

    #constructor for gui
    def __init__(self):

        #super constructor
        super(FormWidget,self).__init__()
        
        #create MenuBars
        self.initializeMenuBar()
                
        #set Window Title
        self.setWindowTitle("Fahrplananzeige")
        #set default error Message
        self.errorMsg="Keine Information  vorhanden"
        #create empty list for station Ids
        self.stationId=[]
        #initialize ConnectionList
        self.conList=ConnectionsList()
        #set filter to active
        self.filterActive=True
        #initalize Widget for map
        self.mapWidget=QMapWidget()
        #initialize SettingsWidget
        self.settingsWidget=SettingsWidget()

        #create HorizontalBoxLayout as overall Widget layout
        layout=qw.QHBoxLayout()

        #intialize three main layout parts
        box1=self.initializeUserInputLayout()
        box2=self.initializeConnectionTableLayout()
        box3=self.initializeDetailsTableLayout()
        
        #add all layouts to form-Layout
        layout.addLayout(box1)
        layout.addLayout(box2)
        layout.addLayout(box3)
        
        #set formLayout
        self.setLayout(layout)

    #initializes MenuBar
    def initializeMenuBar(self):

        #create MenuBar with self as parent
        self.myQMenuBar=qw.QMenuBar(self)
        
        #create Menu for changing settings
        settingsMenu=self.myQMenuBar.addMenu('Einstellung')
        #Create Action for changing settings
        settingsAction=qw.QAction('Ändern',self)
        #connect Action with method
        settingsAction.triggered.connect(self.showSettingsWidget)
        #add Action to Menu
        settingsMenu.addAction(settingsAction)
        
        #create Menu for changing Colors
        colorMenu=self.myQMenuBar.addMenu('Farben')
        #create Action for changing Path color
        colorPathAction=qw.QAction('Pfad-Farbe ändern',self)
        #connect Action with method
        colorPathAction.triggered.connect(self.changePathColor)
        #add Action to Menu
        colorMenu.addAction(colorPathAction)
        #create Action for changing Marker Color
        colorMarkerAction=qw.QAction('Marker-Farbe ändern',self)
        #connect Action with method
        colorMarkerAction.triggered.connect(self.changeMarkerColor)
        #add Action to Menu
        colorMenu.addAction(colorMarkerAction)     
        
        #create Menu for application
        exitMenu=self.myQMenuBar.addMenu('Anwendung')
        #create Action for closing application
        exitAction=qw.QAction('Beenden',self)
        #connect Action with method
        exitAction.triggered.connect(qw.qApp.quit)
        #add Action to Menu
        exitMenu.addAction(exitAction)
        
    #initializes layout for userInput on gui, adds these Widgets to layout
    def initializeUserInputLayout(self):

        #create VerticalBoxLayouts
        layout=qw.QVBoxLayout()

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
        
        #create Horizontal Layout for filtering
        filterLayout=qw.QHBoxLayout()
        #create CheckBoxes for activating Filtering
        self.checkFilter=qw.QCheckBox(" Filter ")
        #create CheckBoxes for choosing filters
        self.checkICE=qw.QCheckBox(" ICE/TGV ")
        self.checkIC=qw.QCheckBox(" IC/EC ")
        self.checkOther=qw.QCheckBox(" other ")
        #add checkboxes to filterLayout
        filterLayout.addWidget(self.checkFilter)
        filterLayout.addWidget(self.checkICE)
        filterLayout.addWidget(self.checkIC)
        filterLayout.addWidget(self.checkOther)
        
        #create Layout for activating map
        mapLayout=qw.QHBoxLayout()
        #create CheckBox for en/disabling map
        self.mapActive=qw.QCheckBox(" Karte anzeigen ")
        #add checkbox to layout
        mapLayout.addWidget(self.mapActive)
                
        #create buttons for getting connections earlier/later and group them
        requestEarlierLater_layout=qw.QHBoxLayout()
        self.earlier=qw.QPushButton("Früher")
        self.later=qw.QPushButton("Später")
        self.later.clicked.connect(self.getConnectionsLater)
        self.earlier.clicked.connect(self.getConnectionsEarlier)
        requestEarlierLater_layout.addWidget(self.earlier)
        requestEarlierLater_layout.addWidget(self.later)
        
        #add layouts and widgets to layout
        layout.addLayout(input1_layout)
        layout.addLayout(input2_layout)
        layout.addWidget(self.date_chooser)
        layout.addLayout(radioButton_layout)
        layout.addLayout(filterLayout)
        layout.addLayout(mapLayout)
        layout.addLayout(requestEarlierLater_layout)
        layout.addLayout(request_layout)
        
        return layout

    #initializes Layout for connectionTable, Label and navigation
    def initializeConnectionTableLayout(self):
        #create VerticalBoxLayout
        layout=qw.QVBoxLayout()

        #label for connectionTable
        self.connection_label=qw.QLabel("")
        #QTableWidget for displaying connections
        self.connectionTable=QConnectionTable(self)
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

        #layout for navigation
        navigation_layout=qw.QHBoxLayout()
        #add buttons to navigation layout        
        navigation_layout.addWidget(self.prev)
        navigation_layout.addWidget(self.reload)
        navigation_layout.addWidget(self.next)
         
        #add widgets and navigationLayout to layout
        layout.addWidget(self.connection_label)
        layout.addWidget(self.connectionTable)
        layout.addLayout(navigation_layout)
        
        return layout
    
    #initializes layout for ConnectionDetails,label
    def initializeDetailsTableLayout(self):
        #create VerticalBoxLayout
        layout=qw.QVBoxLayout()
        
        #label for details of a connection
        self.details_label=qw.QLabel("")
        #QTableWidget for presenting detailed data of a connection
        self.detailsTable=QDetailsTable(self)
        #connect QTableWidget with function
        self.detailsTable.clicked.connect(self.getConnectionsOnClickInDetails)
                
        #add label
        layout.addWidget(self.details_label)
        #add QTableWidget
        layout.addWidget(self.detailsTable)
        #return layout with added widgets
        return layout

    #called on click of detailsTable
    def getConnectionsOnClickInDetails(self):
        #get selected Row in connection details
        row=self.detailsTable.currentRow()
        #avoid error if nothing is selected
        if row<0:
                return
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
    
    #clears detailsTable
    def clearDetailsTable(self):
        self.detailsTable.setRowCount(0)

    #called on click of connectionTable
    #request connection details if needed and displays them  
    def getDetails(self):
        #get the selected Index
        index=self.connectionTable.currentRow()
        #avoid error if nothing was selected
        if index<0:
                return
        #get the connection according to the index
        connection=self.conList.getSingleConnection(self.conList.getDisplayedIndex(),index)
        #if stopList is empty request details information
        if  connection.stopList==[]:
              #get reference link of connection
              urlString=connection.ref
              try:
                    #request xml String
                    xmlString=req.getXMLStringConnectionDetails(urlString)
              except err.HTTPError as e:
                        print('The server couldn\'t fulfill the request.')
                        print('Error code: ', e.code)
                        return
              except err.URLError as e:
                        print('We failed to reach a server.')
                        print('Reason: ', e.reason)
                        return
              stopList=parser.getStopListFromXMLString(xmlString)
              if not stopList=="":
                    #set the stopList of the connection to the local list
                    connection.stopList=stopList
              else:
                    self.details_label.setText(self.errorMsg)
                    return
        #for every stop in stopList add it to QTableWidget
        coordinates=[]
        #clear detailsTable
        self.clearDetailsTable()
        for i in range(len(connection.stopList)):
                self.addStopToDetails(connection.stopList[i])
                coordinates.append(connection.stopList[i].pos)
                if connection.stopList[i].id==connection.stopid:
                        markerIndex=i
        #set details_label text to connection information
        self.details_label.setText(connection.toStringDetails())
        self.conList.setDisplayedDetailedIndex(self.conList.getDisplayedIndex(),index)

        #check if imageData is empty and if map is selected   
        if connection.imageData.isEmpty() and self.mapActive.isChecked():
                #request imageData and create QByteArray and set imageData
                connection.imageData=qc.QByteArray(req.getMapWithLocations(coordinates,markerIndex,self.settingsWidget.settings))
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
              self.clearConnectionTable()
              #for every connection add connection display it
              self.addConnections(self.conList.getConnectionPage(self.conList.getDisplayedIndex()))
              self.setConnectionLabel()      

    def refreshPage(self):
        index =self.conList.getDisplayedIndex()
        if index>=0:
                self.clearConnectionTable()
                self.addConnections(self.conList.getConnectionPage(index))
    
    #clears the connectionTable
    def clearConnectionTable(self):
        self.connectionTable.setRowCount(0)
        
    #next navigation
    def showNextPage(self):
        #on last page do nothing
        #else go one page forward and display
        if self.conList.getDisplayedIndex()<self.conList.getPageCount()-1:
              self.conList.setDisplayedIndex(self.conList.getDisplayedIndex()+1)
              #remove all elements from QTableWidget
              self.clearConnectionTable()
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
        #select first element
        self.connectionTable.selectRow(0)

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
             try:
                     #create xml-object
                     xmlString=req.getXMLStringStationRequest(loc)
             except err.HTTPError as e:
                     print('The server couldn\'t fulfill the request.')
                     print('Error code: ', e.code)
                     return
             except err.URLError as e:
                     print('We failed to reach a server.')
                     print('Reason: ', e.reason)
                     return
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
        hourShift=self.settingsWidget.settings.offSet
        self.getConnectionsWithShiftedTime(-1,hourShift)

    #later means add hours
    def getConnectionsLater(self):
        hourShift=self.settingsWidget.settings.offSet
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
         try: 
                xmlString=req.getXMLStringConnectionRequest(date,time,identifier,isDeparture)
         except err.HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                return
         except err.URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
                return
         connections=parser.getConnectionsFromXMLString(xmlString,isDeparture)
         self.clearConnectionTable()
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

    #create ColorDialog for choosing path color
    def changePathColor(self):
        #create ColorDialog
        colordialog=qw.QColorDialog()
        #get the color
        newColor=colordialog.getColor(qg.QColor(),self,'Pfad-Farbe wählen')
        #check for invalid color
        if newColor.isValid():
                self.settingsWidget.settings.setPathColor(newColor)
    
    #create ColorDialog for choosing marker color
    def changeMarkerColor(self):
        #create ColorDialog
        colordialog=qw.QColorDialog()
        #get the color
        newColor=colordialog.getColor(qg.QColor(),self,'Marker-Farbe wählen')
        #check for invalid color
        if newColor.isValid():
                self.settingsWidget.settings.setMarkerColor(newColor)
                
    #updates and shows settingsWidget
    def showSettingsWidget(self):
              self.settingsWidget.update()          

    #basic keyPressEvent for getting connections
    def keyPressEvent(self,e):
        #enter/return to search stations/connections
        if e.key() == qc.Qt.Key_Return or e.key() == qc.Qt.Key_Enter:
                if self.stationId==[]:
                        self.getStations()
                else:
                        self.getConnectionsNow()
        elif e.key() == qc.Qt.Key_F5:
                self.refreshPage()
        #all other events are passed to the super keyPressEvent
        else:
                super(FormWidget,self).keyPressEvent(e)
                

if __name__=="__main__":
        app=qw.QApplication(sys.argv)
        formwidget=FormWidget()
        formwidget.show()
        sys.exit(app.exec_())

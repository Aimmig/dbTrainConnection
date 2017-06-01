from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg

from Structs import RequestSettings

#class that represents widget for choosing some settings
class SettingsWidget(qw.QWidget):
        
        #set some default values for later use
        mapSizeMin=300
        mapSizeMax=800
        minTimeOffSet=1
        maxTimeOffSet=24
        defaultSize=500
        defaultOffSet=3
        
        #constructor manages layout stuff
        def __init__(self):
        
                #super constructor
                super(SettingsWidget,self).__init__()
                #set window title
                self.setWindowTitle("Einstellungen ändern")
                
                #create global Layout
                layout=qw.QVBoxLayout()
                
                #create validator with valid values
                val=qg.QIntValidator(SettingsWidget.mapSizeMin,SettingsWidget.mapSizeMax)
                #create line edits for width/height with default values
                self.mapWidth=qw.QLineEdit(str(SettingsWidget.defaultSize))
                self.mapHeight=qw.QLineEdit(str(SettingsWidget.defaultSize))
                #set validators
                self.mapWidth.setValidator(val)
                self.mapHeight.setValidator(val)
                
                #layout for map height width
                mapLayout=qw.QHBoxLayout()
                #add descripton label and line Edits to layout
                mapLayout.addWidget(qw.QLabel(" Breite: "))
                mapLayout.addWidget(self.mapWidth)
                mapLayout.addWidget(qw.QLabel(" Höhe: "))
                mapLayout.addWidget(self.mapHeight)
                
                
                #create validator with valid values
                val=qg.QIntValidator(self.minTimeOffSet,self.maxTimeOffSet)
                #create lne edit for offset with default value
                self.offsetField=qw.QLineEdit(str(SettingsWidget.defaultOffSet))
                #set validator
                self.offsetField.setValidator(val)
                self.offsetField.setMaximumWidth(50)
                label=qw.QLabel(" Stunden ")
                label.setMaximumWidth(60)
                self.save=qw.QPushButton("Übernehmen")
                self.save.clicked.connect(self.saveInput)
                
                #add components to layout1
                layout1=qw.QHBoxLayout()
                layout1.addWidget(label)
                layout1.addWidget(self.offsetField)
                layout1.addWidget(self.save)
                
                #add both layout to global layout
                layout.addLayout(mapLayout)
                layout.addLayout(layout1)
                #set layout
                self.setLayout(layout)
                
                #intialize Request settings object with default values
                self.settings=RequestSettings(SettingsWidget.defaultSize,SettingsWidget.defaultOffSet)
        
        #saves userInput to class variables
        def saveInput(self):
                try:
                        #convert desired height and with to int
                        height=int(self.mapHeight.text())
                        width=int(self.mapWidth.text())
                        
                        #TO-DO: Prevent to little values
                        #size to small use default size
                        #if height<SettingsWidget.defaultSize or width<SettingsWidget.defaultSize:
                        #        height=SettingsWidget.defaultSize
                        #        width=SettingsWidget.defaultSize
                        
                        #set settings to values
                        self.settings.setWidth(width)
                        self.settings.setHeight(height)
                #on error do nothing, e.g use old values              
                except ValueError:
                        pass
                try:
                        #convert desired offset
                        offset=int(self.offsetField.text())
                        #set setting to value
                        self.settings.setOffSet(offset)
                #on error do nothing e.g use old value
                except ValueError:
                        pass
                #close widget
                self.close()
        
        #update values in textfield and shows widget
        def update(self):
                #read and convert actuall height from settings and set it
                self.mapHeight.setText(str(self.settings.height))
                #read and convert actuall width from settings and set it 
                self.mapWidth.setText(str(self.settings.width))
                #read and convert actuall offset from settings and set it
                self.offsetField.setText(str(self.settings.offSet))
                self.show() 

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg

from Structs import RequestSettings

class SettingsWidget(qw.QWidget):
        mapSizeMin=300
        mapSizeMax=800
        minTimeOffSet=1
        maxTimeOffSet=24
        defaultSize=500
        defaultOffSet=3
        
        def __init__(self):
                super(SettingsWidget,self).__init__()
                self.setWindowTitle("Einstellungen ändern")
                
                layout=qw.QVBoxLayout()
                mapLayout=qw.QHBoxLayout()
                val=qg.QIntValidator(SettingsWidget.mapSizeMin,SettingsWidget.mapSizeMax)
                self.mapWidth=qw.QLineEdit(str(SettingsWidget.defaultSize))
                self.mapHeight=qw.QLineEdit(str(SettingsWidget.defaultSize))
                self.mapWidth.setValidator(val)
                self.mapHeight.setValidator(val)
                
                mapLayout.addWidget(qw.QLabel(" Breite: "))
                mapLayout.addWidget(self.mapWidth)
                mapLayout.addWidget(qw.QLabel(" Höhe: "))
                mapLayout.addWidget(self.mapHeight)
                
                self.offsetField=qw.QLineEdit(str(SettingsWidget.defaultOffSet))
                val=qg.QIntValidator(self.minTimeOffSet,self.maxTimeOffSet)
                self.offsetField.setValidator(val)
                self.offsetField.setMaximumWidth(50)
                label=qw.QLabel(" Stunden ")
                label.setMaximumWidth(60)
                self.save=qw.QPushButton("Übernehmen")
                self.save.clicked.connect(self.saveInput)
                
                layout1=qw.QHBoxLayout()
                layout1.addWidget(label)
                layout1.addWidget(self.offsetField)
                layout1.addWidget(self.save)
                
                layout.addLayout(mapLayout)
                layout.addLayout(layout1)
                self.setLayout(layout)
                
                self.settings=RequestSettings(SettingsWidget.defaultSize,SettingsWidget.defaultOffSet)

        def saveInput(self):
                #try to convert desired height and with to int
                try:
                        height=int(self.mapHeight.text())
                        width=int(self.mapWidth.text())
                        #TO-DO: Prevent to little values
                        #size to small use default size
                        #if height<SettingsWidget.defaultSize or width<SettingsWidget.defaultSize:
                        #        height=SettingsWidget.defaultSize
                        #        width=SettingsWidget.defaultSize
                        self.settings.setWidth(width)
                        self.settings.setHeight(height)
                #on error use default values               
                except ValueError:
                        pass
                try:
                        offset=int(self.offsetField.text())
                        self.settings.setOffSet(offset)
                except ValueError:
                        pass

        def update(self):
                self.mapHeight.setText(str(self.settings.height))
                self.mapWidth.setText(str(self.settings.width))
                self.offsetField.setText(str(self.settings.offSet))
                self.show() 

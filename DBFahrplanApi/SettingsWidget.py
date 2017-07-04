#    -----------------------------------------------------------------------
#    This program requests connections and corresponding details from the
#    API of Deutsche Bahn and presents them in an user interface
#    This file encapsulates the widget for changing some settings.
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

from PyQt5 import QtWidgets, QtGui
from Structs import RequestSettings


class SettingsWidget(QtWidgets.QWidget):
    """
    Class that represents the widget for changing some
    settings, that might not be changed as frequently
    so they aren't located in the main gui.
    This includes the mapSize and the time offset
    used when requesting connections earlier/later.
    """

    # set some default values for later use
    mapSizeMin = 300
    mapSizeMax = 800
    minTimeOffSet = 1
    maxTimeOffSet = 24
    defaultSize = 500
    defaultOffSet = 3

    # noinspection PyArgumentList
    def __init__(self):
        """
        Constructor manages layout, initializes widget and sets all desired properties.
        """

        # super constructor
        super(SettingsWidget, self).__init__()
        # set window title
        self.setWindowTitle('Einstellungen ändern')

        # create global Layout
        layout = QtWidgets.QVBoxLayout()

        # create validator with valid values
        val = QtGui.QIntValidator(SettingsWidget.mapSizeMin, SettingsWidget.mapSizeMax)
        # create line edits for width/height with default values
        self.mapWidth = QtWidgets.QLineEdit(str(SettingsWidget.defaultSize))
        self.mapHeight = QtWidgets.QLineEdit(str(SettingsWidget.defaultSize))
        # set validators
        self.mapWidth.setValidator(val)
        self.mapHeight.setValidator(val)

        # layout for map height width
        mapLayout = QtWidgets.QHBoxLayout()
        # add description label and line Edits to layout
        mapLayout.addWidget(QtWidgets.QLabel(' Breite: '))
        mapLayout.addWidget(self.mapWidth)
        mapLayout.addWidget(QtWidgets.QLabel(' Höhe: '))
        mapLayout.addWidget(self.mapHeight)

        # create validator with valid values
        val = QtGui.QIntValidator(self.minTimeOffSet, self.maxTimeOffSet)
        # create lne edit for offset with default value
        self.offsetField = QtWidgets.QLineEdit(str(SettingsWidget.defaultOffSet))
        # set validator
        self.offsetField.setValidator(val)
        self.offsetField.setMaximumWidth(50)
        label = QtWidgets.QLabel(' Stunden ')
        label.setMaximumWidth(60)
        self.save = QtWidgets.QPushButton('Übernehmen')
        # noinspection PyUnresolvedReferences
        self.save.clicked.connect(self.saveInput)

        # add components to layout1
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(label)
        layout1.addWidget(self.offsetField)
        layout1.addWidget(self.save)

        # add both layout to global layout
        layout.addLayout(mapLayout)
        layout.addLayout(layout1)
        # set layout
        self.setLayout(layout)

        # initialize Request settings object with default values
        # change this to create object first in constructor and then use values from object instead of
        # member variables
        self.settings = RequestSettings(SettingsWidget.defaultSize, SettingsWidget.defaultOffSet, 'config.txt')

    def getOffSet(self) -> int:
        """
        Returns the offset to use in seconds.
        :rtype int
        """

        return self.settings.offSet * 3600

    def saveInput(self):
        """
        Saves user input (if possible) into class variables.
        """

        try:
            # convert desired height and with to int
            height = int(self.mapHeight.text())
            width = int(self.mapWidth.text())
            # set settings to values
            self.settings.setWidth(width)
            self.settings.setHeight(height)
        # on error do nothing, e.g use old values
        except ValueError:
            pass
        try:
            # convert desired offset
            offset = int(self.offsetField.text())
            # set setting to value
            self.settings.setOffSet(offset)
        # on error do nothing e.g use old value
        except ValueError:
            pass
        # close widget
        self.close()

    def update(self):
        """
        Reads values of class variables and displays them.
        Shows the widget.
        """

        # read and convert actual height from settings and set it
        self.mapHeight.setText(str(self.settings.height))
        # read and convert actual width from settings and set it
        self.mapWidth.setText(str(self.settings.width))
        # read and convert actual offset from settings and set it
        self.offsetField.setText(str(self.settings.offSet))
        self.show()

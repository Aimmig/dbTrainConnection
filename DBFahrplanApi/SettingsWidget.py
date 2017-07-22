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

    # noinspection PyArgumentList
    def __init__(self):
        """
        Constructor manages layout, initializes widget and sets all desired properties.
        """

        # initialize Request from config file
        self.settings = RequestSettings('config.txt')

        # close widget

   # def update(self):
   #     """
   #     Reads values of class variables and displays them.
   #     Shows the widget.
   #     """

   #     # read and convert actual height from settings and set it
   #     self.mapHeight.setText(str(self.settings.height))
   #     # read and convert actual width from settings and set it
   #     self.mapWidth.setText(str(self.settings.width))
   #     # read and convert actual offset from settings and set it
   #     self.offsetField.setText(str(self.settings.offSet))
   #     self.show()

from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc

class QDetailsTable(qw.QTableWidget):
        def __init__(self):
                #define some constants for later use
                self.stop_Index=0
                self.arr_Index=1
                self.dep_Index=2
                self.track_Index=3
                self.header_list=["Halt","Ankunft","Abfahrt","Gleis"]
                self.minimumWidth=420
                self.minimumHeight=320
                super(QDetailsTable,self).__init__()
                #make table not editable
                self.setEditTriggers(qw.QAbstractItemView.NoEditTriggers)
                #make only rows selectable
                self.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
                #make only one row selectable at a time
                self.setSelectionMode(qw.QAbstractItemView.SingleSelection)
                #set numberColumnCount to length of header
                self.setColumnCount(len(self.header_list))
                #set Horizontal Headers
                self.setHorizontalHeaderLabels(self.header_list)
                header=self.horizontalHeader()
                #only stretch colum with stop, resize other columns to contents
                header.setSectionResizeMode(self.stop_Index,qw.QHeaderView.Stretch)
                header.setSectionResizeMode(self.arr_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(self.dep_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(self.track_Index,qw.QHeaderView.ResizeToContents)
                #do not show grid
                self.setShowGrid(False)
                #set minimum Size
                self.setMinimumSize(qc.QSize(self.minimumWidth,self.minimumHeight))
                #set size policy to minimalExpanding
                self.setSizePolicy(qw.QSizePolicy.MinimumExpanding,qw.QSizePolicy.MinimumExpanding)

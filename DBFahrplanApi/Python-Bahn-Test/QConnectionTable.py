from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc

class QConnectionTable(qw.QTableWidget):
        #constructor
        def __init__(self):
                #define some constants for later use
                self.name_Index=0
                self.from_Index=1
                self.to_Index=2
                self.time_Index=3
                self.track_Index=4
                self.header_list=["Zugnummer","von","nach","Uhrzeit","Gleis"]
                self.minimumWidth=420
                self.minimumHeight=320
                #call super constructor
                super(QConnectionTable,self).__init__()
                #set columCount to number of entries in header list
                self.setColumnCount(len(self.header_list))
                #set Horizontal Header for QTableWidget
                self.setHorizontalHeaderLabels(self.header_list)
                #make table not editable
                self.setEditTriggers(qw.QAbstractItemView.NoEditTriggers)
                #only make rows selectable
                self.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
                #only one selection at a time is allowed
                self.setSelectionMode(qw.QAbstractItemView.SingleSelection)
                #do not show grind
                self.setShowGrid(False)
                #do not show vertical Header
                self.verticalHeader().setVisible(False)
                header=self.horizontalHeader()
                #set all Columns to ResizeToConents 
                #only colums with stop names are allowed to stretch
                header.setSectionResizeMode(self.name_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(self.from_Index,qw.QHeaderView.Stretch)
                header.setSectionResizeMode(self.to_Index,qw.QHeaderView.Stretch)
                header.setSectionResizeMode(self.time_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(self.track_Index,qw.QHeaderView.ResizeToContents)
                #set MimimumSize
                self.setMinimumSize(qc.QSize(self.minimumWidth,self.minimumHeight))
                #set Size Policy to MimumExpanding
                self.setSizePolicy(qw.QSizePolicy.MinimumExpanding,qw.QSizePolicy.MinimumExpanding)
                

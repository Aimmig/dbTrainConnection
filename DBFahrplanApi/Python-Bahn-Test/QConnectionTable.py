from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc

class QConnectionTable(qw.QTableWidget):

        #define some constants for later use
        name_Index=0
        from_Index=1
        to_Index=2
        time_Index=3
        track_Index=4
        header_list=["Zugnummer","von","nach","Uhrzeit","Gleis"]
        minimumWidth=420
        minimumHeight=320
       
        #constructor
        def __init__(self):
                #call super constructor
                super(QConnectionTable,self).__init__()
                #set columCount to number of entries in header list
                self.setColumnCount(len(QConnectionTable.header_list))
                #set Horizontal Header for QTableWidget
                self.setHorizontalHeaderLabels(QConnectionTable.header_list)
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
                header.setSectionResizeMode(QConnectionTable.name_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(QConnectionTable.from_Index,qw.QHeaderView.Stretch)
                header.setSectionResizeMode(QConnectionTable.to_Index,qw.QHeaderView.Stretch)
                header.setSectionResizeMode(QConnectionTable.time_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(QConnectionTable.track_Index,qw.QHeaderView.ResizeToContents)
                #set MimimumSize
                self.setMinimumSize(qc.QSize(QConnectionTable.minimumWidth,QConnectionTable.minimumHeight))
                #set Size Policy to MimumExpanding
                self.setSizePolicy(qw.QSizePolicy.MinimumExpanding,qw.QSizePolicy.MinimumExpanding)
                

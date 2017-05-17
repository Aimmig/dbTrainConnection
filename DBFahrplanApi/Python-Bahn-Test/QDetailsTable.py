from PyQt5 import QtWidgets as qw
from PyQt5 import QtCore as qc

class QDetailsTable(qw.QTableWidget):

        #define some constants for later use
        stop_Index=0
        arr_Index=1
        dep_Index=2
        track_Index=3
        header_list=["Halt","Ankunft","Abfahrt","Gleis"]
        minimumWidth=420
        minimumHeight=320

        def __init__(self):
                
                super(QDetailsTable,self).__init__()
                #make table not editable
                self.setEditTriggers(qw.QAbstractItemView.NoEditTriggers)
                #make only rows selectable
                self.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
                #make only one row selectable at a time
                self.setSelectionMode(qw.QAbstractItemView.SingleSelection)
                #set numberColumnCount to length of header
                self.setColumnCount(len(QDetailsTable.header_list))
                #set Horizontal Headers
                self.setHorizontalHeaderLabels(QDetailsTable.header_list)
                header=self.horizontalHeader()
                #only stretch colum with stop, resize other columns to contents
                header.setSectionResizeMode(QDetailsTable.stop_Index,qw.QHeaderView.Stretch)
                header.setSectionResizeMode(QDetailsTable.arr_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(QDetailsTable.dep_Index,qw.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(QDetailsTable.track_Index,qw.QHeaderView.ResizeToContents)
                #do not show grid
                self.setShowGrid(False)
                #set minimum Size
                self.setMinimumSize(qc.QSize(QDetailsTable.minimumWidth,QDetailsTable.minimumHeight))
                #set size policy to minimalExpanding
                self.setSizePolicy(qw.QSizePolicy.MinimumExpanding,qw.QSizePolicy.MinimumExpanding)

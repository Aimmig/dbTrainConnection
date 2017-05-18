from PyQt5 import QtCore as qc

#clas representing a single train connection
class Connection:

    #format date as dd.M.yy
    dateFormat="dd.M.yy"
    #formate time as hh:mm
    timeFormat="hh:mm"
        
    def __init__(self,name,typ,stopid,stopName,time,date,direction,origin,track,ref):
        #Name e.g. IC10250,ICE516, etc
        self.name=name
        #Typ: IC,ICE, EC,..
        self.type=typ
        #id of the station which the connection was requested from        
        self.stopid=stopid
        #name of station which the connection was requested from
        self.stopName=stopName
        #time corresponding to requested connection and station
        self.time=time
        #date of the connection
        self.date=date
        #direction of connection
        self.direction=direction
        #origin of the connection
        self.origin=origin
        #track of the connection corresponding to requested station
        self.track=track
        #reference link for more details
        self.ref=ref
        #list of all Stops of this connection
        self.stopList=[]
        #construct connection with empyt imageData
        self.imageData=qc.QByteArray()

    #returns properly formatted dateString
    def timeToString(self):
        return self.time.toString(Connection.timeFormat)

    #string representation of a connection for details label
    def toStringDetails(self):
        detailsString="Zugverlauf von " + self.name +" am " +self.date.toString(Connection.dateFormat)
        return detailsString

    #genereall String represenatation of a connection for overview
    def toStringGenerall(self):
        res="Fahrplantabelle für "+self.stopName+" am "+self.date.toString(Connection.dateFormat)
        return res
            

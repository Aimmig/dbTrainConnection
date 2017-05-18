from PyQt5 import QtCore as qc

#clas representing a single train connection
class Connection:

    #format date as dd.M.yy
    dateFormat="dd.M.yy"
    #formate time as hh:mm
    timeFormat="hh:mm"
    #string constants for toStringMethods
    departureString=" (Abfahrt) "
    arrivalString=" (Ankunft) "
    detailsBaseString="Zugverlauf von "
    generallBaseString="Fahrplantabelle für "
    datePrefix=" am "
        
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
        res=Connection.detailsBaseString + self.name + Connection.datePrefix +self.date.toString(Connection.dateFormat)
        return res

    #genereall String represenatation of a connection for overview
    def toStringGenerall(self):
        res=Connection.generallBaseString + self.stopName
        if self.origin:
                res+=Connection.departureString
        else:
                res+=Connection.arrivalString
        res+=Connection.datePrefix +self.date.toString(Connection.dateFormat)
        return res

#class representing a single train stop of a connection
class Stop:
    
    #format time with hh:mm
    timeFormat="hh:mm"

    def __init__(self,name,identifier,arrTime,arrDate,depTime,depDate,track,lon,lat):
        #name of the stop-station
        self.name=name
        #id of the stop-station
        self.id=identifier
        #arrival and departure Time and Date
        self.arrTime=arrTime
        self.arrDate=arrDate
        self.depTime=depTime
        self.depDate=depDate
        #Track from wich the connection starts
        self.track=track
        #position of the stop
        self.pos=Coordinate(lon,lat)

    #returns formatted arrTimeDateString
    def arrTimeToString(self):
        return self.arrTime.toString(Stop.timeFormat)
    
    #returns formatted depTimeString
    def depTimeToString(self):
        return self.depTime.toString(Stop.timeFormat)

class Coordinate:

    def __init__(self,lon,lat):
        self.lon=lon
        self.lat=lat 
            

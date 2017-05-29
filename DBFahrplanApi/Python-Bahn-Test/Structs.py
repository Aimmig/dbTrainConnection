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

class Filter:
    
    #member variables are true if this type should be included
    def __init__(self,ICE,IC,other):
        self.ICE=ICE
        self.IC=IC
        self.other=other
        
    def filterICE(self,con):
        return con.type=="ICE" or "ICE" in con.name 
    def filterIC(self,con):
        return con.type==("IC" or "IC" in con.name) and not self.filterICE(con)
    def filterEC(self,con):
        return con.type=="EC" or "EC" in con.name
    def filterTGV(self,con):
        return con.type=="TGV" or "TGV" in con.name 
    def filterOther(self,con):
        return not(self.filterICE(con) or self.filterIC(con) or self.filterEC(con) or self.filterTGV(con))
        
    #this method needs clean-up !!! can be simplified and not cluttered
    def filter(self,connections):
        res=[]
        for i in range(len(connections)):
                selected=False
                if self.ICE:
                        selected=self.filterICE(connections[i]) or self.filterTGV(connections[i])
                if self.IC:
                        selected=selected or self.filterIC(connections[i]) or self.filterEC(connections[i])
                if self.other:
                        selected=selected or self.filterOther(connections[i])
                if selected:
                        res.append(i)
        return res

class ConnectionsList:

    def __init__(self):
        self.connectionPages=[]
        self.displayedIndex=-1
        self.displayedDetailedIndex=(-1,-1)

    def getSingleConnection(self,pageIndex,conIndexOnPage):
        return self.connectionPages[pageIndex][conIndexOnPage]
    def getStop(self,pageIndex,conIndexOnPage,row):
        return self.connectionPages[pageIndex][conIndexOnPage].stopList[row]
    def getConnectionPage(self,pageIndex):
        return self.connectionPages[pageIndex]
    def getPageCount(self):
        return len(self.connectionPages)
    def appendPage(self,connections):
        self.connectionPages.append(connections)
    def getDetailsIndices(self):
        return self.displayedDetailedIndex
    def getDisplayedIndex(self):
        return self.displayedIndex
    def setDisplayedIndex(self,val):
        self.displayedIndex=val
    def setDisplayedDetailedIndex(self,pageIndex,row):
        self.displayedDetailedIndex=(pageIndex,row)

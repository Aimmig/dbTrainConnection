from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg

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

#just for encapsulation of longituted, latitude
class Coordinate:

    #construct coordinate with longituted, latitude
    def __init__(self,lon,lat):
        self.lon=lon
        self.lat=lat

#class for filtering connections based on train type
class Filter:
    
    #member variables are true if this type should be included
    def __init__(self,ICE,IC,other):
        self.ICE=ICE
        self.IC=IC
        self.other=other
    
    #static method for filtering trainType ICE
    @staticmethod
    def filterICE(con):
        return con.type=="ICE" or "ICE" in con.name 
    
    #static method for filtering trainType IC
    @staticmethod
    def filterIC(con):
        return con.type==("IC" or "IC" in con.name) and not Filter.filterICE(con)
    
    #static method for filtering trainType EC
    @staticmethod
    def filterEC(con):
        return con.type=="EC" or "EC" in con.name

    #static method for filtering trainType TGV
    @staticmethod
    def filterTGV(con):
        return con.type=="TGV" or "TGV" in con.name
    
    ##static method for filtering all other train types
    @staticmethod 
    def filterOther(con):
        #connection has train type other if it does not have an above stated train type
        return not(Filter.filterICE(con) or Filter.filterIC(con) or Filter.filterEC(con) or Filter.filterTGV(con))
        
    #filters list of connection based on set train types
    #returns list of originall indices of all train that pass the filter
    def filter(self,connections):
        res=[]
        #iterate over all connections in list
        for i in range(len(connections)):
                #initialy train is not selected
                selected=False
                #for each selected filter type check if connection has this type
                if self.ICE:
                        selected=Filter.filterICE(connections[i]) or Filter.filterTGV(connections[i])
                if self.IC:
                        selected=selected or Filter.filterIC(connections[i]) or Filter.filterEC(connections[i])
                if self.other:
                        selected=selected or Filter.filterOther(connections[i])
                #connection pases filter
                if selected:
                        #add index of connection to list
                        res.append(i)
        #return list of indices
        return res

#class to encapsulate connection data structure and managa indices
class ConnectionsList:

    #construct ConnectionList
    def __init__(self):
        #no information at construction
        self.connectionPages=[]
        #thus indices -1
        self.displayedIndex=-1
        self.displayedDetailedIndex=(-1,-1)

    #returns the single connection with given index on given page
    def getSingleConnection(self,pageIndex,conIndexOnPage):
        return self.connectionPages[pageIndex][conIndexOnPage]

    #returns the i-th stop of the single connection with given index on given Page
    def getStop(self,pageIndex,conIndexOnPage,i):
        return self.getSingleConnection(pageIndex,conIndexOnPage).stopList[i]

    #returns the connectionList (page) with given Index
    def getConnectionPage(self,pageIndex):
        return self.connectionPages[pageIndex]
        
    #returns the amount of pages
    def getPageCount(self):
        return len(self.connectionPages)
     
    #appends connections as page
    def appendPage(self,connections):
        self.connectionPages.append(connections)

    #returns DetailsIndices
    def getDetailsIndices(self):
        return self.displayedDetailedIndex

    #returns DisplayedIndex
    def getDisplayedIndex(self):
        return self.displayedIndex
    
    #sets Displayed index to given value
    def setDisplayedIndex(self,val):
        self.displayedIndex=val
      
    #sets DetailIndices to pageIndex and row
    def setDisplayedDetailedIndex(self,pageIndex,row):
        self.displayedDetailedIndex=(pageIndex,row)

#class that encapsulate all important settings for requesting
#like mapOptions and offset        
class RequestSettings:

    #static settings that can not be changed (at the moment)
    MARKER_SIZE='small'
    MARKER_SIZE_SPECIAL='mid'
    PATH_SIZE='3'
    MARKER_COLOR_SPECIAL=qg.QColor('#aa339988')
    MIN_SIZE=300
            
    #initialize changeable settings with default Values
    def __init__(self,defaultSize,defaultOffSet):
        self.PATH_COLOR=qg.QColor('#ff0000')
        self.MARKER_COLOR=qg.QColor('#5555BB')
        self.height=defaultSize
        self.width=defaultSize
        self.offSet=defaultOffSet
    
    #retunrs string repr. of PathColor that can be used in urls
    def formatPathColor(self):
        return self.PATH_COLOR.name().replace('#','0x')
    
    #retunrs string repr. of MarkerColor that can be used in urls
    def formatColor(self):
        return self.MARKER_COLOR.name().replace('#','0x')

    #retunrs string repr. of MarkerColorSpecial that can be used in urls
    def formatSpecialColor(self):
        return RequestSettings.MARKER_COLOR_SPECIAL.name().replace('#','0x')
    
    #set MarkerColor to given color
    def setMarkerColor(self,col):
        self.MARKER_COLOR=col

    #set PathColor to given color
    def setPathColor(self,col):
        self.PATH_COLOR=col
    
    #set height to given value
    def setHeight(self,h):
        #prevent to small size
        if h>=RequestSettings.MIN_SIZE:
                self.height=h
        else:
                self.height=RequestSettings.MIN_SIZE

    #set width to given value
    def setWidth(self,w):
        #prevent to small size
        if w>=RequestSettings.MIN_SIZE:
                self.width=w
        else:
                self.width=RequestSettings.MIN_SIZE

    #set offset to given value
    def setOffSet(self,s):
        #do not set invalid offsets
        if s<=0:
                return
        self.offSet=s

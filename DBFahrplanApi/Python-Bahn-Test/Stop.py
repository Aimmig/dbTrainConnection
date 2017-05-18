from PyQt5 import QtCore as qc

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


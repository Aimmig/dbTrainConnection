from PyQt5 import QtCore as qc

#class representing a single train stop of a connection
class Stop:

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
        #Longitude and latiude of the station
        self.lon=lon
        self.lat=lat

    #String representation of arrival Time
    def arrTimeToString(self):
        timeString=str(self.arrTime.hour())+":"+str(self.arrTime.minute())
        return timeString
    
    #String representation of departure Time
    def depTimeToString(self):
        timeString=str(self.depTime.hour())+":"+str(self.depTime.minute())
        return timeString


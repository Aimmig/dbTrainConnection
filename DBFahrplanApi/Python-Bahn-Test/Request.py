import urllib.request as url_req
import urllib.error as err
from PyQt5 import QtCore as qc

KEY="DBhackFrankfurt0316"
LANGUAGE="de"
BASE_URL="https://open-api.bahn.de/bin/rest.exe/"

#returns the XML-String 
def getXMLStringConnectionDetails(urlString):
        req=url_req.Request(urlString)
        try:
            with url_req.urlopen(req) as response:
                result=response.read()
                return result
        except err.HTTPError as e:
             print('The server couldn\'t fulfill the request.')
             print('Error code: ', e.code)
        except err.URLError as e:
             print('We failed to reach a server.')
             print('Reason: ', e.reason)
        return ""
        

#returns the XML-String representation of the requested ressource
def getXMLStringStationRequest(loc):
        url=createStationRequestURL(loc)
        req=url_req.Request(url)
        try:
            with url_req.urlopen(req) as response:
                result=response.read()
                return result
        except err.HTTPError as e:
             print('The server couldn\'t fulfill the request.')
             print('Error code: ', e.code)
        except err.URLError as e:
             print('We failed to reach a server.')
             print('Reason: ', e.reason)
        return ""

#returns the XML-String representation of the Connection Request
def getXMLStringConnectionRequest(date,time,identifier,isDeparture):
        url=createConnectionRequestURL(date,time,identifier,isDeparture)
        req=url_req.Request(url)
        try:
            with url_req.urlopen(req) as response:
                result=response.read()
                return result
        except err.HTTPError as e:
             print('The server couldn\'t fulfill the request.')
             print('Error code: ', e.code)
        except err.URLError as e:
             print('We failed to reach a server.')
             print('Reason: ', e.reason)
        return ""

#creates the URL for requesting Connections
def createConnectionRequestURL(date,time,identifier,isDeparture):
        #build date-String
        dateString=str(date.year())+"-"+str(date.month())+"-"+str(date.day())
        #build and encode timeString
        timeString=str(time.hour())+"%3A"+str(time.minute())
        #build last part of url
        lastPart="authKey="+KEY+"&lang="+LANGUAGE+"&id="
        lastPart=lastPart+str(identifier)+"&date="+dateString+"&time"+timeString
        #build complete url
        if isDeparture:
             return BASE_URL+"departureBoard?"+lastPart
        else:
             return BASE_URL+"arrivalBoard?"+lastPart

#creates the URL for requesting Stations
def createStationRequestURL(loc):
        return BASE_URL+"location.name?authKey="+KEY+"&lang="+LANGUAGE+"&input="+loc

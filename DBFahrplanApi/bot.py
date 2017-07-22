import sys
import time
import telepot
from telepot.loop import MessageLoop

from PyQt5 import QtCore, QtGui, QtWidgets
from Widgets import QConnectionTable, QDetailsTable, QMapWidget
from Request import Request
from Structs import Connection, ConnectionsList, Stop, Filter, Coordinate, RequestSettings
from XMLParser import XMLParser as parser
import sys
import urllib.error as err

settings = RequestSettings('config.txt')
connections = []

def handle(msg):
    global connections
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    
    try:
        index=int(msg['text'])
        details = Request.getXMLStringConnectionDetails(connections[index].ref)
        stop_details = parser.getStopListFromXMLString(details)
        result = ''
        for s in stop_details:
               result = result + s.name + ' ' + s.depTimeToString(settings) + ' Gleis: ' + s.track +'\n'
        bot.sendMessage(chat_id,result)
        return
    except ValueError:
        pass
    
    if content_type == 'text':
        loc = msg['text']
        # check for empty input
        if loc.strip():
            try:
                # create xml-object
                xmlString = Request.getXMLStringStationRequest(loc, settings)
            except err.HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                return
            except err.URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
                return
            (newStations, newStationsId) = parser.getStationsFromXMLString(xmlString)
            # if something was actually found replace everything
            if newStations:
                #bot.sendMessage(chat_id, newStations)
                test_id = newStationsId[0]
                # noinspection PyArgumentList
                date = QtCore.QDate.currentDate()
                # noinspection PyArgumentList
                time = QtCore.QTime.currentTime()
                try:
                       xmlString = Request.getXMLStringConnectionRequest(date, time, test_id, True, settings)
                except err.HTTPError as e:
                       print('The server couldn\'t fulfill the request.')
                       print('Error code: ', e.code)
                       return
                except err.URLError as e:
                       print('We failed to reach a server.')
                       print('Reason: ', e.reason)
                       return
                connections = parser.getConnectionsFromXMLString(xmlString,True)
                conn_string = ''
                i = 0
                for c in connections:
                       conn_string = conn_string + str(i)+' : nach ' + c.direction + ' um ' + c.timeToString(settings) + ' Gleis: ' + c.track + '\n'
                       i = i+1
                bot.sendMessage(chat_id,conn_string)

TOKEN = '330294771:AAFJAZ5oyvNZX8nrJiDeqVCSTfrtsiy6IoA'

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)

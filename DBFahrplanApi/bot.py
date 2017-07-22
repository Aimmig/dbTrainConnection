import time
import telepot
from telepot.loop import MessageLoop

from PyQt5 import QtCore
from Request import Request
from Structs import RequestSettings
from XMLParser import XMLParser as parser
import urllib.error as err

settings = RequestSettings('config.txt')
connections = []


def getStationId(loc):
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
        if newStations:
            return newStationsId[0], newStations[0]


def getConnections(identifier, isDeparture):
    global connections
    # noinspection PyArgumentList
    current_date = QtCore.QDate.currentDate()
    # noinspection PyArgumentList
    current_time = QtCore.QTime.currentTime()
    try:
        xmlString = Request.getXMLStringConnectionRequest(current_date, current_time, identifier, isDeparture, settings)
    except err.HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        return
    except err.URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        return
    connections = parser.getConnectionsFromXMLString(xmlString, isDeparture)


def sendConnections(chat_id, isDeparture, name):
    global connections
    if isDeparture:
        conn_string = 'Abfahrten für ' + name + '\n'
    else:
        # noinspection SpellCheckingInspection
        conn_string = 'Ankunften für ' + name + '\n'
    i = 0
    if isDeparture:
        for c in connections:
            conn_string = conn_string + str(i) + ': ' + c.name + ' nach ' + c.direction + ', ' + c.timeToString(
                settings) + ', Gleis ' + c.track + '\n'
            i = i + 1
    else:
        for c in connections:
            conn_string = conn_string + str(i) + ': ' + c.name + ' von ' + c.origin + ', ' + c.timeToString(
                settings) + ', Gleis ' + c.track + '\n'
            i = i + 1
    bot.sendMessage(chat_id, conn_string)


def sendDetails(chat_id, index_string):
    try:
        index = int(index_string)
        details = Request.getXMLStringConnectionDetails(connections[index].ref)
        stop_details = parser.getStopListFromXMLString(details)
        # noinspection SpellCheckingInspection
        result = 'Verlauf von ' + connections[index].name + ' am ' + connections[index].dateToString(settings) + '\n'
        for s in stop_details:
            timeString = s.depTimeToString(settings)
            if not timeString:
                timeString = s.arrTimeToString(settings)
            if s.track:
                track = ', Gleis ' + s.track
            else:
                track = ''
            result = result + s.name + ', ' + timeString + track + '\n'
        bot.sendMessage(chat_id, result)
    except ValueError:
        pass
    except IndexError:
        pass


def handle(msg):
    global connections
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        split_msg = msg['text'].split(' ')
        if len(split_msg) == 2:
            if split_msg[0] == '/info':
                sendDetails(chat_id, split_msg[1])
                return
            if split_msg[0] == '/departure':
                isDeparture = True
            elif split_msg[0] == '/arrival':
                isDeparture = False
            else:
                return
            identifier, name = getStationId(split_msg[1])
            getConnections(identifier, isDeparture)
            sendConnections(chat_id, isDeparture, name)


# noinspection SpellCheckingInspection
TOKEN = '330294771:AAFJAZ5oyvNZX8nrJiDeqVCSTfrtsiy6IoA'
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
# Keep the program running.
while 1:
    time.sleep(10)

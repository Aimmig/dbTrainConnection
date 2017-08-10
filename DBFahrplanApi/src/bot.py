import time
import telepot
from telepot.loop import MessageLoop

from PyQt5 import QtCore
from Request import Request
from Structs import RequestSettings
from XMLParser import XMLParser as parser
import urllib.error as err

settings = RequestSettings('../config.txt')
connections = []


def getStationId(loc: str) -> (int, str):
    """
    Returns id and name of most suitable train station to given location
    :type loc str
    :rtype (int,str)
    """

    # avoid empty string
    if loc.strip():
        try:
            # create xml-object
            xmlString = Request.getXMLStringStationRequest(loc, settings)
        except err.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            return 0, ''
        except err.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            return 0, ''
        # parse information into list of id and names
        (newStations, newStationsId) = parser.getStationsFromXMLString(xmlString)
        #
        if newStations:
            return newStationsId[0], newStations[0]
        else:
            return 0, ''


# noinspection PyArgumentList
def getConnections(identifier, isDeparture, current_time=QtCore.QTime.currentTime(),
                   current_date=QtCore.QDate.currentDate()):
    """
    Retrieves connections
    :type identifier int
    :type isDeparture bool
    :type current_date: QtCore.QDate
    :type current_time: QtCore.QTime
    """

    global connections
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
        conn_string = 'Ankunften für ' + name + '\n'
    i = 1
    for c in connections:
            conn_string = conn_string + str(i) + ': ' + c.toString(settings) + '\n'
            i = i + 1
    bot.sendMessage(chat_id, conn_string)


def sendDetails(chat_id, index_string):
    try:
        index = int(index_string) - 1
        details = Request.getXMLStringConnectionDetails(connections[index].ref)
        stop_details = parser.getStopListFromXMLString(details)
        result = 'Verlauf von ' + connections[index].name + ' am ' + connections[index].dateToString(settings) + '\n'
        for s in stop_details:
            result = result + s.toString(settings) + '\n'
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
            if split_msg[0].lower() == '/info':
                sendDetails(chat_id, split_msg[1])
                return
            if split_msg[0].lower() == '/departure':
                isDeparture = True
            elif split_msg[0].lower() == '/arrival':
                isDeparture = False
            else:
                return
            identifier, name = getStationId(split_msg[1])
            if name:
                getConnections(identifier, isDeparture)
                sendConnections(chat_id, isDeparture, name)
                return
        if len(split_msg) == 3:
            if split_msg[0].lower() == '/departure':
                isDeparture = True
            elif split_msg[0].lower() == '/arrival':
                isDeparture = False
            else:
                return
            identifier, name = getStationId(split_msg[1])
            if name:
                req_time = QtCore.QTime.fromString(split_msg[2], settings.timeFormat)
                getConnections(identifier, isDeparture, req_time)
                sendConnections(chat_id, isDeparture, name)
                return
        if len(split_msg) == 4:
            if split_msg[0].lower() == '/departure':
                isDeparture = True
            elif split_msg[0].lower() == '/arrival':
                isDeparture = False
            else:
                return
            identifier, name = getStationId(split_msg[1])
            if name:
                req_time = QtCore.QTime.fromString(split_msg[2], settings.timeFormat)
                date = QtCore.QDate.fromString(split_msg[3], settings.dateFormat)
                if not date.isValid():
                    # noinspection PyArgumentList
                    current_date = QtCore.QDate.currentDate()
                    year = current_date.year()
                    date = QtCore.QDate.fromString(split_msg[3]+'.'+str(year), settings.dateFormat)
                getConnections(identifier, isDeparture, req_time, date)
                sendConnections(chat_id, isDeparture, name)
                return

# noinspection SpellCheckingInspection
TOKEN = '330294771:AAFJAZ5oyvNZX8nrJiDeqVCSTfrtsiy6IoA'
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
# Keep the program running.
while 1:
    time.sleep(10)

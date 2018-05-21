# README #

### What is this repository for? ###

This is a project to display train connections from DB (Germany) using their rest-API.
In adittion the application shows the stops of a train connection on a map using google-Maps-Static Api
I originall wrote the project in Java using Swing, but because that sucked i decided to port
it to Python3 using PyQt5.

### How do I get set up? ###
You need to have installed Pyhton3 as well as PyQt5.
Inside the configs directory create a key.txt, where you need to the api-keys. This includes
the api key for google-maps-static api and the key for DB-Fahrplan-Api 
(see http://data.deutschebahn.com/dataset/api-fahrplan for more information).

Layout of the keys.txt needs to be like this:

[Keys]
# Key for db-api
DBKey = YOURKEYHERE
# Key for GoogleMaps-static-api
GoogleMapsKey = YOURKEYHERE

### How to contribute? ###
If you want to contribute feel free, to bring your ideas and implement them.
Therefore please contact me so, that we can discuss about it.
Some error handling is missing when Requesting the information from the web.
Some functionality from the Java version still needs to be ported to Python.

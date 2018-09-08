# README #

### What is this repository for? ###

This is a project to display train connections from DB (Germany) using their rest-API.
In adittion the application shows the stops of a train connection on a customizable map
using MabBox (see https://www.mapbox.com or https://www.mapbox.com/api-documentation for
more infos). For more information on dbopendata see https://github.com/dbopendata/openbahn or
https://github.com/dbopendata/db-fahrplan-api

### Previous versions ###
Previous version of this used the Google Maps Static API. But Google recently made it,
so you need to pay for every request. So I searched and found MapBox (based on OpenStreetMap)
which is free and even more customizable.

### Needed software/installations ##
As this whole project is based on python3 and pyqt5, you need to have installed them.
I recommend using python 3.6 or higher and pyqt5.8 or higher. Besides that, you need to 
install polyline (handling path encondings) for python3 and urllib3 (handling web request).

### API Keys ###
For access to the rest-API of DB you need get an api-key (see 
http://data.deutschebahn.com/dataset/api-fahrplan). Just mail them and thats it.
To use the mapbox you also need an api key. Just go to https://www.mapbox.com and register;
then you'll find your standard api key.

### Configuration ###
Inside the configs directory create a key.txt file, where you need to the place those api-keys.
Layout of the keys.txt needs to be like this:

[Keys]

DBKey = YOURKEYHERE

GoogleMapsKey = YOURKEYHERE

Inside the config.txt file one can change some default settings.
The en.txt and de.txt are some language files. Those are currenlty NOT used everywhere, but
some parts work with them.

### How to contribute? ###
If you want to contribute feel free, to bring your ideas and implement them.
Therefore you can contact me so, that we can discuss about it.

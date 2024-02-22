import json
import requests
stops = []
favourites = []

def getStops():
    host = 'https://smartinfo.ivb.at/api/JSON/STOPS'
    response = requests.get('%s/' % (host)).json()
    for entry in response:
        stop = entry["stop"]
        stops.append(stop)

def getDepartures(stops):
    for stop in stops:
        host = f"https://smartinfo.ivb.at/api/JSON/PASSAGE?stopID={stop['uid']}"
        response = requests.get('%s' % (host)).json()
        departures = []
        for entry in response:
            if entry.get('smartinfo') != None:
                departure = entry.get('smartinfo')
                departures.append(departure)
        stop['departures'] = departures
    return stops

def saveStops():
    datei = open('IVB/stops.json', 'w')
    json.dump(stops, datei)

def suche(suchbegriff):
    found_data = []
    for stop in stops:
        if suchbegriff.lower() in stop['name'].lower():
            found_data.append(stop)
    return found_data

def printStops(stops):
    if len(stops) > 0:
        for stop in stops:
            print(f"uid: {stop['uid']}; name: {stop['name']}")
    else:
        print("Keine Daten vorhanden")
def printDepartures(stops):
    if len(stops) > 0:
        for stop in stops:
            print(f"uid: {stop['uid']}; name: {stop['name']}")
            for i in range(5):
                print(f"Zeit: {stop['departures'][i]['time']}; nach: {stop['departures'][i]['direction']}")
                
def readStops():
        with open('IVB/stops.json') as json_file:
            global stops
            stops = []
            stops = json.load(json_file)  

if __name__ =='__main__':
    getStops()
    saveStops()
    while True:
        i = input('\n\n(1) Haltestellen suchen\n(2) Favoriten hinzufügen\n(3) Favoriten anzeigen\n(4) Beenden\n')
        if i == '1':
            suchbegriff = input('Suchbegriff: ')
            haltestellen = suche(suchbegriff)
            haltestellen = getDepartures(haltestellen)
            printDepartures(haltestellen)
            readStops()
        elif i == '2':
            suchbegriff = input('Suchbegriff: ')
            haltestellen = suche(suchbegriff)
            for haltestelle in haltestellen:
                favourites.append(haltestelle)
                readStops()
        elif i == '3':
            haltestellen = getDepartures(favourites)
            printDepartures(haltestellen)
            readStops()
        elif i == '4':
            break
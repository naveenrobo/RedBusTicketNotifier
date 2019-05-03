import requests
import re
import datetime
import urllib
import csv

from city import City

# Get id for given location
# https://www.redbus.in/Home/SolarSearch?search=salem

# Get bus list given the location and date
# https://www.redbus.in/search/SearchResults?fromCity=123&toCity=141&src=Chennai&dst=Coimbatore&DOJ=06-May-2019&meta=true&returnSearch=0
#post : {headers: {Content-Type: "application/json"}}

# Get seats
# https://www.redbus.in/search/seatlayout/12329432/01-May-2019/18112?isRedDealApplicable=false

# URL's
search = 'https://www.redbus.in/Home/SolarSearch?search=%s'

# other varialbes
now = datetime.datetime.now()
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "July", "Aug", "Sept", "Oct", "Nov", "Dec"]


def getRequest(url):
    r = requests.get(url)
    if(r.status_code == 200):
        try:
            content = r.json()
            return content
        except Exception as e:
            print(e)
    else:
        print("error while loading page.Response code is %s" % r.status_code)
        return None


def postRequest(url, payload, headers, querystring):
    r = requests.request("POST", url, data=payload,
                         headers=headers, params=querystring)
    if(r.status_code == 200):
        try:
            content = r.json()
            return content
        except Exception as e:
            print(e)
    else:
        print("error while loading page.Response code is %s" % r.status_code)
        print(r.text)
        print(r.url)
        return None


def getCityDetails(url):
    try:
        result = getRequest(url)
        if(result['response']['numFound'] > 0):
            city = result['response']['docs']
            if(city != None):
                src = City(city[0]['ID'], city[0]['Name'])
                return src
            print("Location not found")
            return City(0, "Location not found")
    except Exception as e:
        print(e)


def getCityId(fromLocation, toLocation):
    print("Searching cities for it's id...{fromLoc} to {toLoc}".format(
        fromLoc=fromLocation, toLoc=toLocation))
    src = getCityDetails(search % fromLocation)
    dest = getCityDetails(search % toLocation)
    return src, dest


def getTravelDate():
    day = input("Enter day ({}): ".format(now.strftime("%d"))) or now.day
    month = input("Enter month ({}):".format(now.strftime("%m"))) or now.month
    year = input("Enter year ({}): ".format(now.strftime("%Y"))) or now.year
    monthString = ""
    try:
        day = int(day)
        monthString = months[int(month)]
        year = int(year)
    except Exception:
        raise Exception("Invalid date")

    date = "{day}-{month}-{year}".format(day=day,
                                         month=monthString, year=year)

    return date


def currentDate():
    return "{day}-{month}-{year}".format(day=now.day, month=months[int(now.month)], year=now.year)


def findBus(fromLocation, toLocation, date, busName, ac, sleeper):
    src, dest = getCityId(fromLocation, toLocation)
    if(src is not None and dest is not None):
        print(src.name)
        print(dest.name)
        busSearch = 'https://www.redbus.in/search/SearchResults'
        queryString = {'fromCity': src.id, 'toCity': dest.id, 'src': src.name,
                       'dst': dest.name,  'DOJ': date, 'meta': 'true', 'returnSearch': '0'}
        payload = "{\"headers\":{\"Content-Type\":\"application/json\"}}"
        headers = {
            'Content-Type': "application/json"
        }
        buses = postRequest(busSearch, payload, headers, queryString)
        busList = []
        if(buses is not None):
            print("Searching through the list")
            list = buses['inv']
            for bus in list:
                if(busName is not None and busName.lower() in bus['Tvs'].lower()):
                    print(bus['bc']['IsAc'] and bus['bc']['IsSleeper'])
                    if(bus['bc']['IsAc'] is bool(ac) and bus['bc']['IsSleeper'] is bool(sleeper)):
                        busList.append(bus)
        
        return busList


def gatherData():
    fromLocation = input('Enter source location : ')
    toLocation = input('Enter destination location : ')
    date = currentDate()
    while True:
        try:
            date = getTravelDate()
            break
        except Exception:
            print("\nInvalid date\n")
            continue
    print("\nTravel date is %s" % date)
    busName = input('Enter Bus name : ') or None
    return fromLocation, toLocation, date, busName


if __name__ == "__main__":
    print("Running file directly")
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            print(findBus(line['from'],line['to'],line['date'],line['busname'],line['ac'],line['sleeper']))

    #findBus(fromLocation, toLocation, date, busName)

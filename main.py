import requests
import re
import datetime

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
        print("error while loading page.Response code is "+r.status_code)
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
        month = months[int(month)]
        year = int(year)
    except Exception:
        raise Exception("Invalid date")

    date = "{day}-{month}-{year}".format(day=day,
                                         month=monthString, year=year)

    return date


def currentDate():
    return "{day}-{month}-{year}".format(day=now.day, month=months[int(now.month)], year=now.year)


if __name__ == "__main__":

    print("Running file directly")

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

    src, dest = getCityId(fromLocation, toLocation)
    if(src is not None and dest is not None):
        print(src.name)
        print(dest.name)

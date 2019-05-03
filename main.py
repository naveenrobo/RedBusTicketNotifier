import requests
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
            return City(0,"Location not found")
    except Exception as e:
        print(e)


def getCityId(fromLocation, toLocation):
    print("Searching cities for it's id...{fromLoc} to {toLoc}".format(
        fromLoc=fromLocation, toLoc=toLocation))
    src = getCityDetails(search % fromLocation)
    dest = getCityDetails(search % toLocation)
    return src, dest


if __name__ == "__main__":
    print("Running file directly")
    fromLocation = input('Enter source location : ')
    toLocation = input('Enter destination location : ')
    src, dest = getCityId(fromLocation, toLocation)
    print(src.name)
    print(dest.name)

# import requests
from itertools import filterfalse
from re import X
import math
import geocoder
import math
import requests
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter



def change_in_latitude(currentLat,distance):
    degreeToMiles = 68.875
    changeInLat = distance/degreeToMiles
    return currentLat+changeInLat

def change_in_longitude(currentLong, lat, distance):
    rad180 = math.pi / 180
    lode = 69.172 # length of degree equator
    degreeToMiles = math.cos(lat*rad180) * lode
    change = distance / degreeToMiles
    return currentLong + change
    #https://gis.stackexchange.com/questions/142326/calculating-longitude-length-in-miles
    # Length of 1 degree of Longitude = cosine (latitude in decimal degrees) * length of degree (miles) at equator.

def getStationList(range, latitude, longitude, fuelTypeId, carMPG):
    minLat = round(change_in_latitude(latitude, -(range/2)), 4) #minLat
    minLng = round(change_in_longitude(longitude, minLat,-(range/2)), 4) #minLng
    maxLat = round(change_in_latitude(latitude, range/2),4) #maxLat
    maxLng = round(change_in_longitude(longitude, maxLat,range/2),4) #maxLng
    gasParam = {
        "minLat" : minLat,
        "minLng" : minLng,
        "maxLat" : maxLat,
        "maxLng": maxLng,
        "fuelTypeId" : str(fuelTypeId),
        "height" : 600,
        "width" :1265
    }
    response = requests.post('https://www.gasbuddy.com/gaspricemap/map', json=gasParam)
    data = response.json()
    primaryStations = data['primaryStations']
    secondaryStations = data['secondaryStations']
  
    filteredPrimary = [station for station in primaryStations if not station['price'] == '--'] #Removes stations where no price
    filteredSecondary = [station for station in secondaryStations if not station['price'] == '--']
    df = pd.json_normalize(filteredPrimary) # Adds to dataframe
    df2 = pd.json_normalize(filteredSecondary)
    results = pd.concat([df,df2],ignore_index = True) #Merges primary stations and secondary stations
    calculatedDistance = pd.DataFrame(columns=['id', 'price','distance','calcPrice', 'address'])
    locator = Nominatim(user_agent="GassedUp")
    for index, rows in results.iterrows():
        distance = round(geodesic((rows['lat'],rows['lng']),(latitude, longitude)).miles,2)
        calculatedPrice = round(((float(rows['price']) * distance) / float(carMPG))+float(rows['price']),2)
        coords = str(rows['lat']) + ", " + str(rows['lng'])
        location = locator.reverse(coords)
        calculatedDistance.loc[index] = [rows['id'], rows['price'], distance, calculatedPrice, location.address]
    calculatedDistance = calculatedDistance.sort_values(by=['calcPrice'])
    calculatedDistance.to_csv('stationList.csv', index=False)


def getLocation(address):
    locator = Nominatim(user_agent="GassedUp")
    location = locator.geocode(address)
    return location.latitude, location.longitude 







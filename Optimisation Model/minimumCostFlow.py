from processOverTime import processTripsOverTime
from getAndProcessData import getAndProcessData
import pandas as pd 
import numpy as np
import geopandas as gpd

"""
trips,bikeStations = getAndProcessData()

## Duration Calculations ## 
first = trips["Start Date"].min()
last = trips["Start Date"].max()
def diff(start, end):
    x = pd.to_datetime(end) - pd.to_datetime(start)
    return int(x / np.timedelta64(1, 'W'))
weeks = diff(first,last)
months = weeks /4
days = weeks * 7 

bikeStations = processTripsOverTime(trips,bikeStations,weeks,range(0,7),"W")
bikeStations.to_pickle("bikestations.pkl")

"""


bikeStations = pd.read_pickle("bikestations.pkl")
bikeStations = gpd.GeoDataFrame(bikeStations,crs="EPSG:4326",geometry=gpd.points_from_xy(bikeStations.lon, bikeStations.lat) )

supply = bikeStations[ bikeStations['demand'] <0]
demand = bikeStations [ bikeStations['demand'] > 0]
edges = [] 
print(supply)
print(demand)
def reassignId(x,row):
    x = (x,row)
for index , row in supply.iterrows():
    temp = bikeStations.copy()
    temp['id'] = temp['id'].map()
    print(temp)

import math
from processOverTime import processTripsOverTime
from getAndProcessData import getAndProcessData
import pandas as pd 
import numpy as np
import geopandas as gpd
import pyproj 
from math import radians, cos, sin, asin, sqrt

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

print()
bikeStations = pd.read_pickle("bikestations.pkl")
bikeStations = gpd.GeoDataFrame(bikeStations,crs="EPSG:4326",geometry=gpd.points_from_xy(bikeStations.lon, bikeStations.lat) )
bikeStations = bikeStations.to_crs(crs = pyproj.CRS("EPSG:27700"))
supply = bikeStations[ bikeStations['demand'] <0]
demand = bikeStations [ bikeStations['demand'] > 0]
startEdge = []
startGeo = [] 
endEdge = [] 
endGeo = []
print(supply)
print(demand)

def reassignId(x,row):
    x = (x,row)
for index , row in supply.iterrows():
    for i , r in demand.iterrows():
        if row['id'] != r['id']:
            startEdge.append(row['id'])
            startGeo.append(row.geometry)
            endEdge.append(r['id'])
            endGeo.append(r.geometry)


#edgeids in form supply, demand 
d = {'edgeStart' : startEdge,'startPoint': gpd.GeoSeries(startGeo),'edgeEnd' :endEdge,'endPoint':gpd.GeoSeries(endGeo)}
edges = pd.DataFrame(data=d)
x =   gpd.GeoSeries(edges['startPoint'],crs=pyproj.CRS("EPSG:27700"))
y = gpd.GeoSeries(edges['endPoint'],crs= pyproj.CRS("EPSG:27700"))
distances = x.distance(y,align=False)


edges['weight'] = distances
edges =  edges.drop("startPoint", axis=1)
edges = edges.drop("endPoint", axis=1)
print(edges)


sourceEnds = []
sourceStarts = [-1 for x in range(0,len(supply))]
sourceDistances = [0 for x in range(0,len(supply))] 
for index,row in supply.iterrows():
    sourceEnds.append(row['id'])
d = {'edgeStart':sourceStarts,'edgeEnd':sourceEnds,'weight':sourceDistances}
sourceEdges = pd.DataFrame(data = d )
edges = pd.concat([sourceEdges,edges])

sinkStarts = [] 
sinkEnds = [-2 for x in range (0 ,len(demand))] 
sinkDistances = [0 for x in range(0,len(demand))]

for index,row in demand.iterrows():
    sinkStarts.append(row['id'])


d = {'edgeStart':sinkStarts,'edgeEnd':sinkEnds,'weight':sinkDistances}


sinkEdges = pd.DataFrame(data = d)

edges = pd.concat([sinkEdges,edges])
print(edges)
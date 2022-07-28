import math

from getAndProcessData import getAndProcessData
from processOverDay import processTripsOverTime
import pandas as pd 
import numpy as np
import geopandas as gpd
import pyproj 
from minCostFlowSolver import MinCostFlow
import pdb




"""
trips,bikeStations = getAndProcessData()
bikeStations.to_pickle("bikestations.pkl")

"""


bikeStations = pd.read_pickle("bikestationsraw.pkl")
bikeStations['demand'] = 0 
trips = pd.read_pickle("trips.pkl")
print(trips)
print(bikeStations)
print(trips['Start Date'].min ())
bikeStations = processTripsOverTime(trips,bikeStations,trips['Start Date'].min())
print(bikeStations)

bikeStations = gpd.GeoDataFrame(bikeStations,crs="EPSG:4326",geometry=gpd.points_from_xy(bikeStations.lon, bikeStations.lat) )
bikeStations = bikeStations.to_crs(crs = pyproj.CRS("EPSG:27700"))
supply = bikeStations[ bikeStations['demand'] <0]
demand = bikeStations [ bikeStations['demand'] > 0]

startEdge = []
startGeo = [] 
endEdge = [] 
endGeo = []

demand['demand'] = demand.apply(lambda x : math.ceil(x['demand']),axis = 1 )
supply['demand'] = supply.apply(lambda x : math.floor(x['demand']),axis = 1 )
print(supply['demand'].sum())
print(demand['demand'].sum())
pdb.set_trace()

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
edges['capacity'] = 1
print(edges)


sourceEnds = []
sourceStarts = [-1 for x in range(0,len(supply))]
sourceDistances = [0 for x in range(0,len(supply))] 
#sourceCap = [ 2 for x ]
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
nodes = pd.concat([demand,supply])
print(demand)

idSet = nodes['id'].to_list()
demandSet = nodes['demand'].to_list()
net = []
for x in idSet:
    if x == -1:
        net.append(len(demand))
    if x == -2:
        net.append(-len(demand))
print(idSet)
print(demandSet)


edgeId = []
edgeWeight = []
edgeCap = [] 

for index,row in edges.iterrows():
    edgeId.append((row['edgeStart'],row['edgeEnd']))
    edgeWeight.append(row['weight'])
    edgeCap.append(row['capacity'])
print(edgeId)
print(edgeWeight)
print(edgeCap)
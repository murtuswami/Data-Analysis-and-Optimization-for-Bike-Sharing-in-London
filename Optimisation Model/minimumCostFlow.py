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

print(trips['Start Date'].min ())
bikeStations = processTripsOverTime(trips,bikeStations,trips['Start Date'].min())


bikeStations = gpd.GeoDataFrame(bikeStations,crs="EPSG:4326",geometry=gpd.points_from_xy(bikeStations.lon, bikeStations.lat) )
bikeStations = bikeStations.to_crs(crs = pyproj.CRS("EPSG:27700"))
supply = bikeStations[ bikeStations['demand'] <0]
demand = bikeStations [ bikeStations['demand'] > 0]

startEdge = []
startGeo = [] 
endEdge = [] 
endGeo = []
capacity = [] 
#demand['demand'] = demand.apply(lambda x : math.ceil(x['demand']),axis = 1 )
#supply['demand'] = supply.apply(lambda x : math.floor(x['demand']),axis = 1 )
print(supply['demand'].sum())
print(demand['demand'].sum())

#Supply -> Demand 

for index , row in supply.iterrows():
    for i , r in demand.iterrows():
        if row['id'] != r['id']:
            startEdge.append(row['id'])
            startGeo.append(row.geometry)
            endEdge.append(r['id'])
            endGeo.append(r.geometry)
            capacity.append(abs(row['demand']))



#edgeids in form supply, demand 
d = {'edgeStart' : startEdge,'startPoint': gpd.GeoSeries(startGeo),'edgeEnd' :endEdge,'endPoint':gpd.GeoSeries(endGeo),'capacity':capacity}
edges = pd.DataFrame(data=d)
x =   gpd.GeoSeries(edges['startPoint'],crs=pyproj.CRS("EPSG:27700"))
y = gpd.GeoSeries(edges['endPoint'],crs= pyproj.CRS("EPSG:27700"))
distances = x.distance(y,align=False)
edges['weight'] = distances
edges =  edges.drop("startPoint", axis=1)
edges = edges.drop("endPoint", axis=1)




sourceEnds = []
sourceStarts = [-1 for x in range(0,len(supply))]
sourceDistances = [0 for x in range(0,len(supply))] 

sourceCap = []
bikeStations = bikeStations.set_index('id')

for index,row in supply.iterrows():
  
    sourceEnds.append(row['id'])
    sourceCap.append(abs(row['demand']))


d = {'edgeStart':sourceStarts,'edgeEnd':sourceEnds,'weight':sourceDistances,'capacity':sourceCap}
sourceEdges = pd.DataFrame(data = d )
edges = pd.concat([sourceEdges,edges])

sinkStarts = [] 
sinkEnds = [-2 for x in range (0 ,len(demand))] 
sinkDistances = [0 for x in range(0,len(demand))]
sinkCap = []
for index,row in demand.iterrows():
    sinkStarts.append(row['id'])
    sinkCap.append(row['demand'])

d = {'edgeStart':sinkStarts,'edgeEnd':sinkEnds,'weight':sinkDistances,'capacity':sinkCap}

sinkEdges = pd.DataFrame(data = d)

edges = pd.concat([sinkEdges,edges])



nodes = pd.concat([demand,supply])
nodes = nodes.set_index('id')
nodes['imbalance']= 0
nodes = nodes['imbalance'].to_frame()


nodes.loc[-1] = [abs(supply['demand'].sum())]
nodes.loc[-2] = [-demand['demand'].sum()]


edges = edges.set_index(['edgeStart','edgeEnd'])
print(nodes)
print(edges)

    
"""
for index,row in edges.iterrows():
    edgeId.append((row['edgeStart'],row['edgeEnd']))
    edgeWeight.append(row['weight'])
    edgeCap.append(row['cap'])




nodes is a dataframe containing id as index and imbalance as column 
edges are a dataframe containing [start,end] as index with weights and capacities
    
"""
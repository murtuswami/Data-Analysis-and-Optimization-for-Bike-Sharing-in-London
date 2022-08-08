import math

from getAndProcessData import getAndProcessData
from processOverDay import processTripsOverDate
import pandas as pd 
import numpy as np
import geopandas as gpd
import pyproj 
from minCostFlowSolver import MinCostFlow
import pdb
from pyomo.environ import value
from FeasibleFlowModel import FeasibleFlow
from TSPOR import TSPORSolver
import pickle

"""
trips,bikeStations = getAndProcessData()
bikeStations.to_pickle("bikestations.pkl")

"""
bikeStationsData = pd.read_pickle("bikestationsraw.pkl")
bikeStationsData['demand'] = 0 
trips = pd.read_pickle("trips.pkl")

unq = trips["Start Date"].map(pd.Timestamp.date).unique()

print(len(unq))

routes = []
routeDistances = [] 
for i in unq:

    bikeStations = processTripsOverDate(trips.copy(),bikeStationsData.copy(),i)
    print(bikeStations)
    
    bikeStations = gpd.GeoDataFrame(bikeStations,crs="EPSG:4326",geometry=gpd.points_from_xy(bikeStations.lon, bikeStations.lat) )
    bikeStations = bikeStations.to_crs(crs = pyproj.CRS("EPSG:27700"))
    supply = bikeStations[ bikeStations['demand'] <0]
    demand = bikeStations [ bikeStations['demand'] > 0]

    startEdge = []
    startGeo = [] 
    endEdge = [] 
    endGeo = []
    capacity = [] 

    print(supply['demand'].sum())
    print(demand['demand'].sum())

    for index , row in supply.iterrows():
        for i , r in demand.iterrows():
            if row['id'] != r['id']:
                startEdge.append(row['id'])
                startGeo.append(row.geometry)
                endEdge.append(r['id'])
                endGeo.append(r.geometry)
                capacity.append(abs(row['demand']))


    d = {'edgeStart' : startEdge,'startPoint': gpd.GeoSeries(startGeo),'edgeEnd' :endEdge,'endPoint':gpd.GeoSeries(endGeo),'capacity':capacity}
    edges = pd.DataFrame(data=d)
    x =   gpd.GeoSeries(edges['startPoint'],crs=pyproj.CRS("EPSG:27700"))
    y = gpd.GeoSeries(edges['endPoint'],crs= pyproj.CRS("EPSG:27700"))
    distances = x.distance(y,align=False)
    edges['weight'] = distances
    edges =  edges.drop("startPoint", axis=1)
    edges = edges.drop("endPoint", axis=1)

    edgesWithoutSourceSink = edges.copy()


    distances
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

    nodes['id'] = nodes['id'].astype(np.unicode_)
    nodes = nodes.set_index('id')
    nodes['imbalance']= 0
    nodes = nodes['imbalance'].to_frame()
    nodes.loc["-1"] = [abs(supply['demand'].sum())]
    nodes.loc["-2"] = [-demand['demand'].sum()]

    edges['edgeStart'] = edges['edgeStart'].astype(np.unicode_)
    edges['edgeEnd'] = edges['edgeEnd'].astype(np.unicode_)    
    edges = edges.set_index(['edgeStart','edgeEnd'])

    solver = FeasibleFlow(nodes,edges)
    solver.makeModel()
    results,model = solver.solve()

    keyEdgesDict = {}
    for v in model.X:
        if model.X[v].value !=0 and v[0] != "-1" and v[1] != "-2":
            keyEdgesDict.update({( str(v[0]), str(v[1]) ):int(edges.loc[v]['weight'])})
    edgesDict = {}
    for x in edges.iterrows():
        edgesDict.update({ (str(x[0][0]) ,str(x[0][1])):int(round(x[1]['weight']))})
    TSPSolver = TSPORSolver(keyEdgesDict,edgesDict)
    cost,route = TSPSolver.solve()
    routeDistances.append(route)
    routes.append(route)
with open('routes.pkl', 'wb') as f:
    pickle.dump(routes, f)
with open('routeDistances', 'wb') as f:
    pickle.dump(routeDistances, f)
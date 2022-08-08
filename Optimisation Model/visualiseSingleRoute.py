
import pandas as pd


import pdb
import numpy as np
import pickle
from TSPOR import TSPORSolver
import geopandas as gpd
import folium
from folium.plugins import AntPath
import osmnx as ox
import networkx as nx

with open('keyEdgesDict.p', 'rb') as fp:
    keyEdges = pickle.load(fp)
with open('edgesDict.p','rb') as fp:
    allEdges = pickle.load(fp)
bikeStations= pd.read_pickle("bikestationsraw.pkl")
bikeStations = gpd.GeoDataFrame(bikeStations,crs="EPSG:4326",geometry=gpd.points_from_xy(bikeStations.lon, bikeStations.lat) )
bikeStations['id'] = bikeStations['id'].astype(str)
bikeStations = bikeStations.set_index('id')

print(bikeStations)
TSPSolver = TSPORSolver(keyEdges,allEdges)
cost,route = TSPSolver.solve()

print(cost,route)

route_lats_longs =  [ [ bikeStations.loc[x].lat,bikeStations.loc[x].lon] for x in route ]


map = folium.Map(location = [51.5073219, -0.1276474], tiles='cartodbdark_matter' , zoom_start = 13 )
folium.PolyLine(route_lats_longs,color="blue", weight=2.5, opacity=0.3).add_to(map)
map.save("singleVehicleRoute.html")
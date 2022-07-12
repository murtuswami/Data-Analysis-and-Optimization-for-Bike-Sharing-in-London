from turtle import circle
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import osmnx as ox
import folium 
from folium import plugins
from folium.plugins import HeatMap

url="https://api.tfl.gov.uk/bikepoint"
c= pd.read_json(url)
bikeStations = gpd.GeoDataFrame(c,crs="EPSG:4326",geometry=gpd.points_from_xy(c.lon, c.lat) )
bdb = bikeStations.total_bounds #minx, miny, maxx, maxy 
print(bikeStations)

map = folium.Map(location = [51.5073219, -0.1276474], tiles='OpenStreetMap' , zoom_start = 13)
folium.TileLayer('cartodbdark_matter').add_to(map)
circleStyle = folium.CircleMarker(color = "#F4F6F7", radius=2)

points = folium.features.GeoJson(bikeStations.to_json(),marker = circleStyle)
map.add_child(points)

map.save("map_1.html")



"""
G = ox.graph_from_bbox(bdb[3], bdb[1], bdb[2], bdb[0],network_type='all') # Max y , min y , max x min x  , network_type='drive'
fig, ax = ox.plot_graph(
    G,
    show=False,
    close=False,
    bgcolor="#d6d6d6",
    edge_color="black",
    edge_linewidth=0.3,
    node_size=0,
)
bikeStations.plot(ax = ax,markersize =5, color = "blue", marker ="o",label="Bike Station")
plt.show()
"""
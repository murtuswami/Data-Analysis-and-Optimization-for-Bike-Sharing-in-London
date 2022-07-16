import getAndProcessData
from folium.plugins import MarkerCluster,MousePosition
import folium 
from folium import plugins
import pandas as pd
import getAndProcessData
import processOverTime
import clusterMapper
import numpy as np
from shapely.geometry import Polygon
import geopandas as gpd

trips,bikeStations = getAndProcessData.getAndProcessData()
## Duration Calculations ## 
first = trips["Start Date"].min()
last = trips["Start Date"].max()
def diff(start, end):
    x = pd.to_datetime(end) - pd.to_datetime(start)
    return int(x / np.timedelta64(1, 'W'))
weeks = diff(first,last)
## Add Demand column to bikestations frame ## 



bikeStations = processOverTime.processTripsOverTime(trips,bikeStations,weeks,range(0,6),"W")
map = clusterMapper.mapClusters(bikeStations)
formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
MousePosition(
position="topright",
separator=" | ",
empty_string="NaN",
lng_first=True,
num_digits=20,
prefix="Coordinates:",
lat_formatter=formatter,
lng_formatter=formatter,
    ).add_to(map)

lonList = [-0.18,-0.154,-0.148,-0.14,-0.13,-0.109,-0.105,-0.1,-0.09,-0.074,-0.074,-0.078,-0.117,-0.127,-0.14,-0.148,-0.162,-0.174,-0.18]
latList = [51.5,51.518,51.52,51.521,51.523,51.522,51.524,51.523,51.527,51.524,51.509,51.5,51.497,51.493,51.493,51.492,51.489,51.494,51.495]
print(len(lonList))
print(len(latList))
polygon_geom = Polygon(zip(lonList, latList))
crs = {'init': 'epsg:4326'}
polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])       

polygon.to_file(filename='polygon.geojson', driver='GeoJSON')
polygon.to_file(filename='polygon.shp', driver="ESRI Shapefile")


fg_poly = folium.FeatureGroup(name = "Poly", show = True)
folium.GeoJson(polygon).add_to(fg_poly)
folium.LatLngPopup().add_to(fg_poly)
fg_poly.add_to(map)
map.add_child(folium.LayerControl())
map.save("weeklyClusterWithPolygon"+ ".html")



#We want a chart, showing the average number of bikes entering and exiting central london 




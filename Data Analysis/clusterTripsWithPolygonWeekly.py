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
import createCentralSupplyPolygon
trips,bikeStations = getAndProcessData.getAndProcessData()
## Duration Calculations ## 
first = trips["Start Date"].min()
last = trips["Start Date"].max()
def diff(start, end):
    x = pd.to_datetime(end) - pd.to_datetime(start)
    return int(x / np.timedelta64(1, 'W'))
weeks = diff(first,last)
## Add Demand column to bikestations frame ## 



bikeStations = processOverTime.processTripsOverTime(trips,bikeStations,weeks,range(0,7),"W")
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

polygon,poly_geom = createCentralSupplyPolygon.createPoly()
fg_poly = folium.FeatureGroup(name = "Poly", show = True)
folium.GeoJson(polygon).add_to(fg_poly)
folium.LatLngPopup().add_to(fg_poly)
fg_poly.add_to(map)
map.add_child(folium.LayerControl())

map.save("weeklyClusterWithPolygon"+ ".html")


#We want a chart, showing the average number of bikes entering and exiting central london 




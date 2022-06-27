import requests 
import pandas as pd
import geopandas as gpd
import json


url="https://api.tfl.gov.uk/bikepoint"
c= pd.read_json(url)
bikeStations = gpd.GeoDataFrame(c,crs="EPSG:4326",geometry=gpd.points_from_xy(c.lon, c.lat) )
bdb = bikeStations.total_bounds #minx, miny, maxx, maxy 
#G = ox.graph_from_bbox(bdb[3], bdb[1], bdb[2], bdb[0],network_type='all') # Max y , min y , max x min x  , network_type='drive'
url = "https://api.openstreetmap.org/api/0.6/map?bbox="+ str(bdb[1])+","+ str(bdb[0])+","+  str(bdb[3]) +","+ str(bdb[2]) 
print(url)
response = requests.get(url)

print(response.status_code)
print(response.reason)
#text = json.dumps(response.json(), sort_keys=True, indent=4)
#print(text)

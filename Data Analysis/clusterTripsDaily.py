import pandas as pd
import getAndProcessData
import processOverTime
import clusterMapper
import numpy as np
import folium

trips,bikeStations = getAndProcessData.getAndProcessData()

## Duration Calculations ## 
first = trips["Start Date"].min()
last = trips["Start Date"].max()
def diff(start, end):
    x = pd.to_datetime(end) - pd.to_datetime(start)
    return int(x / np.timedelta64(1, 'W'))
weeks = diff(first,last)
months = weeks /4
days = weeks * 7 


## Add Demand column to bikestations frame ## 
bikeStations = processOverTime.processTripsOverTime(trips,bikeStations,days,range(1,25),"D")
map = clusterMapper.mapClusters(bikeStations)
map.add_child(folium.LayerControl())
map.save("dailyCluster.html")


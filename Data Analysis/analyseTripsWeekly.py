import pandas as pd
import getAndProcessData
import processOverTime
import clusterMapper
import numpy as np


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
bikeStations = processOverTime.processTripsOverTime(trips,bikeStations,weeks,range(0,6),"W")
clusterMapper.mapClusters(bikeStations,"weeklyCluster")






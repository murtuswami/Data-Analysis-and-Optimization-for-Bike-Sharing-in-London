
#We want a chart, showing the average number of bikes entering and exiting central london 
# So in the form of 
# hr, bikes  in 
#another one in the form of 
# hr, bikes out 

import getAndProcessData

import pandas as pd
import getAndProcessData
import numpy as np
import createCentralSupplyPolygon
import geopandas as gpd
import pdb
import numpy 

trips,bikeStations = getAndProcessData.getAndProcessData()
bikeStations = gpd.GeoDataFrame(bikeStations,crs="EPSG:4326",geometry=gpd.points_from_xy(bikeStations.lon, bikeStations.lat) )
polygon,pg = createCentralSupplyPolygon.createPoly()

print(bikeStations) 
bikeStations.set_index('id',inplace = True)
bikeStations.index = bikeStations.index.astype(numpy.int64, copy=True)

def pointInPoly(x):
    if pg.contains(x):
        return True
    return False 


print(bikeStations)

print(trips)

print (bikeStations.index.dtype)

## Duration Calculations ## 
first = trips["Start Date"].min()
last = trips["Start Date"].max()
def diff(start, end):
    x = pd.to_datetime(end) - pd.to_datetime(start)
    return int(x / np.timedelta64(1, 'W'))
weeks = diff(first,last)

#remove trips which start or end at stations for which we have no data 

trips  = trips[trips['StartStation Id'].isin(bikeStations.index)]
trips  = trips[trips['EndStation Id'].isin(bikeStations.index)]

print(trips)

tripsIntoPolygon = []
tripsOutOfPolygon = [] 
tripsWithinPolygon = [] 
for i in range(1,24):
    timeMask = (trips['End Date'].dt.hour >= i) & (trips['End Date'].dt.hour < i +1) & (trips['Start Date'].dt.hour >= i) & (trips['Start Date'].dt.hour < i +1)
    relevantTrips = trips[timeMask]
    tip = relevantTrips[relevantTrips.apply(lambda x: 
        (pointInPoly(bikeStations.loc[x['EndStation Id']].geometry) == True )
        & (pointInPoly(bikeStations.loc[x['StartStation Id']].geometry) == False),axis=1)]
    top = relevantTrips[relevantTrips.apply(lambda x: 
       ( pointInPoly(bikeStations.loc[x['EndStation Id']].geometry) == False)
        & (pointInPoly(bikeStations.loc[x['StartStation Id']].geometry) == True),axis=1)]

    twp = relevantTrips[relevantTrips.apply(lambda x:  
        (pointInPoly(bikeStations.loc[x['EndStation Id']].geometry) == True)
        & (pointInPoly(bikeStations.loc[x['StartStation Id']].geometry) == True),axis=1)]

    print(tip.shape[0],top.shape[0],twp.shape[0])
    print(tip)
    print(top)
    print(twp)
    tripsIntoPolygon.append(tip.shape[0])
    tripsOutOfPolygon.append(top.shape[0])
    tripsWithinPolygon.append(twp.shape[0])

tripsIntoPolygon = np.array(tripsIntoPolygon)
tripsOutOfPolygon = np.array(tripsOutOfPolygon)
tripsWithinPolygon = np.array(tripsWithinPolygon)

tripsIntoPolygon.tofile("tripsintopoly.txt",sep =',')
tripsOutOfPolygon.tofile("tripsoutofpoly.txt",sep=',')
tripsWithinPolygon.tofile("tripswithinpoly.txt",sep = ',')
    
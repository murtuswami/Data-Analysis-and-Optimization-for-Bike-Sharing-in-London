
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

 


## Duration Calculations ## 
first = trips["Start Date"].min()
last = trips["Start Date"].max()
def diff(start, end):
    x = pd.to_datetime(end) - pd.to_datetime(start)
    return int(x / np.timedelta64(1, 'W'))
weeks = diff(first,last)

range = range(0,24)
av = weeks*7

#remove trips which start or end at stations for which we have no data 

trips  = trips[trips['StartStation Id'].isin(pd.Series(bikeStations.index))]
trips  = trips[trips['EndStation Id'].isin(pd.Series(bikeStations.index))]



range = range(0,24)
av = weeks*7

def average(f,n):
    return f/n
tripsStartingInPoly = [] 
tripsEndingInPoly = []
demandInPolyAtTime = [] 
demandInPoly= 0 
print(bikeStations)
for i in range:
    timeMaskEnd = (trips['End Date'].dt.hour >= i) & (trips['End Date'].dt.hour < i +1)
    timeMaskStart = (trips['Start Date'].dt.hour >= i) & (trips['Start Date'].dt.hour < i +1)
    print(timeMaskEnd)
    ##Apply time masks and count the occurences of trips starting and ending in the hour for all trips 
    endFrame= trips[timeMaskEnd]
    endFrameCounts = endFrame['EndStation Id'].value_counts()
    startFrame = trips[timeMaskStart]
    startFrameCounts = startFrame['StartStation Id'].value_counts()

    #trips starting in polygon 
    startFrameCountsInPoly = startFrameCounts.copy().to_frame(name ="count").reset_index()
    m= startFrameCountsInPoly.apply( lambda x:pg.contains(bikeStations.loc[x['index']].geometry),axis=1)
    startFrameCountsInPoly = startFrameCountsInPoly[m]

    #trips ending in polygon 
    endFrameCountsInPoly = endFrameCounts.copy().to_frame(name ="count").reset_index()
    m= endFrameCountsInPoly.apply( lambda x:pg.contains(bikeStations.loc[x['index']].geometry),axis=1)
    endFrameCountsInPoly = endFrameCountsInPoly[m]
    
    print(endFrameCountsInPoly)
    print(startFrameCountsInPoly)
    tripsStartingInPoly.append( startFrameCountsInPoly['count'].sum())
    tripsEndingInPoly.append(endFrameCountsInPoly['count'].sum())
    demandInPoly =  demandInPoly + startFrameCountsInPoly['count'].sum() - endFrameCountsInPoly['count'].sum()
    demandInPolyAtTime.append(demandInPoly)
    

    # Merge bikestations with counted occurences of start and end
    #First Merge ending occurences, use left to ignore invalid ids( -1 ) this creates a column called 'endstation id' in bikestations 
    # which is the number of bikes ending at a locations
    # For columns with no endstations, set the count to 0 using fillna
 
    
    bikeStations= pd.merge(bikeStations, endFrameCounts, how='left', left_index = True,right_index= True)   
    bikeStations['EndStation Id'] = bikeStations['EndStation Id'].fillna(0)
    bikeStations['demand'] -= bikeStations['EndStation Id']                                             #Minus demand from number of bikes ending as it creates a surplus 
    bikeStations = bikeStations.drop('EndStation Id',1)       
    
                                                                                                   # Drop the counts once combined with endstationid 
    bikeStations= pd.merge(bikeStations, startFrameCounts, how='left',left_index=True, right_index= True)
    bikeStations['StartStation Id'] = bikeStations['StartStation Id'].fillna(0)
    bikeStations['demand'] += bikeStations['StartStation Id']                                           #Same for startstationid but instead add to demand since bikes are leaving 
    bikeStations = bikeStations.drop('StartStation Id',1)
    print(endFrameCounts[48],startFrameCounts[48],bikeStations.loc[48]['demand'])
    print( startFrameCounts.sum() -  endFrameCounts.sum(), bikeStations['demand'].sum())
    
print(tripsEndingInPoly)
print(tripsStartingInPoly)
print(demandInPolyAtTime)

    


tripsEndingInPoly = np.array(tripsEndingInPoly)
tripsStartingInPoly = np.array(tripsStartingInPoly)
demandInPolyAtTime = np.array(demandInPolyAtTime)

tripsEndingInPoly.tofile("tripsEndingInPoly.txt",sep =',')
tripsStartingInPoly.tofile("tripsStartingInPoly.txt",sep=',')
demandInPolyAtTime.tofile("demandInPolyAtTime.txt",sep = ',')


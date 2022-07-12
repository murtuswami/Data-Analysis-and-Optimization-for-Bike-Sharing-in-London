from turtle import end_fill
import pandas as pd
import glob
import os 
import numpy as np
import pdb
import geopandas as gpd
import folium 
from folium import plugins
from folium.plugins import HeatMap,HeatMapWithTime,MarkerCluster


##  Read data on bikestations  ## 
url="https://api.tfl.gov.uk/bikepoint"
bikeStations = pd.read_json(url)

## Read data on bike trips recursively from all files 
def idGenerator(x):
    return x.split("_")[1]
bikeStations.id = np.vectorize(idGenerator)(bikeStations.id)
folders =  [x[0] for x in os.walk(os.getcwd() + "/_TfL Cycling Data")]
folders.pop(0)
li = []
for path in folders:
    all_files = glob.glob(path+  "/*.csv")
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
    
frame = pd.concat(li, axis=0, ignore_index=True)


## Bike Trip data manipulation 
frame[['EndStation Id']] = frame[['EndStation Id']].fillna(value=-1) # Endstations have some empty values, fill with -1 
frame['EndStation Id'] = frame['EndStation Id'].astype(np.int64)     # Cast as int as empty values default to float 
frame[['End Date','Start Date']] = frame[['End Date','Start Date']].apply(lambda _: pd.to_datetime(_,format = "%d/%m/%Y %H:%M")) # Convert dates to datetime objects 

## Duration Calculations ## 
first = frame["Start Date"].min()
last = frame["Start Date"].max()
def diff(start, end):
    x = pd.to_datetime(end) - pd.to_datetime(start)
    return int(x / np.timedelta64(1, 'W'))
weeks = diff(first,last)
days = weeks * 7 

## Add Demand column to bikestations frame ## 
bikeStations["demand"] = 0 



heatMapIndex= [] # Holds index values for folium map 
heatDataFrames = [] # Dataframe for each timestep in form [lat, lon ,demand ]

min = 0 #smallest demand value in all dataframe for scaling 
max = 0 #Largest demand value in all dataframes for scaling 

def average(f,n):
    return f/n

for i in range (1,25):
    print(i)
    
    ##Masks for start and end hours##
    timeMaskEnd = (frame['End Date'].dt.hour >= i) & (frame['End Date'].dt.hour < i +1)
    timeMaskStart = (frame['Start Date'].dt.hour >= i) & (frame['Start Date'].dt.hour < i +1)
   
    ##Apply time masks and count the occurences of trips starting and ending in the hour for all trips 
    endFrame= frame[timeMaskEnd]
    endFrameCounts = endFrame['EndStation Id'].value_counts().to_frame()
    startFrame = frame[timeMaskStart]
    startFrameCounts = startFrame['StartStation Id'].value_counts().to_frame()

    ##Average the counts over the number of days## 
    #print(endFrameCounts)
    endFrameCounts['EndStation Id'] = average(endFrameCounts['EndStation Id'],days)
    startFrameCounts['StartStation Id'] = average(startFrameCounts['StartStation Id'],days)
    #print(endFrameCounts)
    ## Data Wrangling 
    # Map index types to string for merge operation and reduce to just counts 
    
    endFrameCounts.index = endFrameCounts.index.map(str)
    startFrameCounts.index = startFrameCounts.index.map(str)
    endFrameCounts = endFrameCounts['EndStation Id']
    startFrameCounts = startFrameCounts['StartStation Id']


    # Merge bikestations with counted occurences of start and end
    #First Merge ending occurences, use left to ignore invalid ids( -1 ) this creates a column called 'endstation id' in bikestations 
    # which is the number of bikes ending at a locations
    # For columns with no endstations, set the count to 0 using fillna
    bikeStations= pd.merge(bikeStations, endFrameCounts, how='left', left_on='id',right_index= True)   
    bikeStations['EndStation Id'] = bikeStations['EndStation Id'].fillna(0)
    bikeStations['demand'] -= bikeStations['EndStation Id']                                             #Minus demand from number of bikes ending as it creates a surplus 
    bikeStations = bikeStations.drop('EndStation Id',1)                                                 # Drop the counts once combined with endstationid 
    bikeStations= pd.merge(bikeStations, startFrameCounts, how='left', left_on='id',right_index= True)
    bikeStations['StartStation Id'] = bikeStations['StartStation Id'].fillna(0)
    bikeStations['demand'] += bikeStations['StartStation Id']                                           #Same for startstationid but instead add to demand since bikes are leaving 
    bikeStations = bikeStations.drop('StartStation Id',1)
    

    
    heatList = bikeStations[["lat","lon","demand"]]
    localMin =  heatList['demand'].min()
    localMax =  heatList['demand'].max()
    min = localMin   if  localMin < min else min
    max = localMax if localMax > max else max 

    ##Append dataframe with demand to list 
    heatDataFrames.append(heatList.copy())
    heatMapIndex.append(i)




def minMaxScaling(series,min,max):
   return (series - min) / (max - min)

print(min)
print(max)

"""
## Seperate into demand and supply ##
def extractDemand(n):
    if n<0:
        return 0 
    return n

def extractSupply(n):
    if n> 0:
        return 0
    return n

demandData = [x.copy() for x in heatDataFrames]
for x in demandData:
    x['demand'] = x['demand'].map(extractDemand)
    x['demand'] = x['demand'].map(lambda x: minMaxScaling(x,min = 0,max= max))
supplyData = [x.copy() for x in heatDataFrames]
for x in supplyData:
     x['demand'] = x['demand'].map(extractSupply)
     x['demand'] = x['demand'].map(abs)
     x['demand'] = x['demand'].map(lambda x: minMaxScaling(x,min = 0,max= max))


print(heatDataFrames)
print("--------------------------------------------------------------------------------")
print(demandData)
print("--------------------------------------------------------------------------------")
print(supplyData)

## Folium HeatMap Display 
print(bikeStations)
map = folium.Map(location = [51.5073219, -0.1276474], tiles='OpenStreetMap' , zoom_start = 13 )
folium.TileLayer('cartodbdark_matter').add_to(map)
marker_cluster = MarkerCluster(control=False).add_to(map)
bikeStations['geocode'] = [[bikeStations['lat'][i],bikeStations['lng'][i]] for i in range(len(df)) ]
folium.Marker(df['geocode']).add_to(marker_cluster)


map.save("24hoursdemandmarkers.html")

demandData = [x.values.tolist() for x in demandData]
supplyData = [x.values.tolist() for x in supplyData]

map = folium.Map(location = [51.5073219, -0.1276474], tiles='OpenStreetMap' , zoom_start = 13 )
folium.TileLayer('cartodbdark_matter').add_to(map)

HeatMapWithTime(demandData,heatMapIndex).add_to(map)
map.save("24hoursAvgDemandMap.html")

map2 = folium.Map(location = [51.5073219, -0.1276474], tiles='OpenStreetMap' , zoom_start = 13 )
folium.TileLayer('cartodbdark_matter').add_to(map2)

HeatMapWithTime(supplyData,heatMapIndex).add_to(map2)
map2.save("24hoursAvgSupplyMap.html")







#heatDataList = [x.values.tolist() for x in heatDataFrames]
#print(heatDataList)








#Step through times hourly, starting from 0000 and ending at 2300. 
#Adjust bike stations delta at each time step. 
"""
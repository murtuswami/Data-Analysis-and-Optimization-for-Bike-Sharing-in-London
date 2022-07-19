
import pandas as pd

def processTripsOverTime(trips,bikeStations,av,range,t):
    bikeStations = bikeStations.copy()
    def average(f,n):
        return f/n
    for i in range:
        ##Masks for start and end hours##""
        if t == "W":
            timeMaskEnd = (trips['End Date'].dt.day_of_week >= i) & (trips['End Date'].dt.day_of_week  < i +1)
            timeMaskStart = (trips['Start Date'].dt.day_of_week  >= i) & (trips['Start Date'].dt.day_of_week  < i +1)
        if t =="D":
            timeMaskEnd = (trips['End Date'].dt.hour >= i) & (trips['End Date'].dt.hour < i +1)
            timeMaskStart = (trips['Start Date'].dt.hour >= i) & (trips['Start Date'].dt.hour < i +1)
        
        ##Apply time masks and count the occurences of trips starting and ending in the hour for all trips 
        endFrame= trips[timeMaskEnd]
        endFrameCounts = endFrame['EndStation Id'].value_counts().to_frame()
        startFrame = trips[timeMaskStart]
        startFrameCounts = startFrame['StartStation Id'].value_counts().to_frame()
       
    
        ##Average the counts over the number of days## 
        #print(endFrameCounts)
        endFrameCounts['EndStation Id'] = average(endFrameCounts['EndStation Id'],av )
        startFrameCounts['StartStation Id'] = average(startFrameCounts['StartStation Id'],av)
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
   
    return bikeStations

     
    
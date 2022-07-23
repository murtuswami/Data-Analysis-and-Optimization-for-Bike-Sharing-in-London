import pandas as pd
import glob
import os 
import numpy as np
""" 
Gets data on bike stations and trips, perform data wrangling and processing 

input: 
Return: DataFrame containing bikestations and Dataframe containing trips with datetime object
"""
def getAndProcessData():
    ##  Read data on bikestations  ## 
    url="https://api.tfl.gov.uk/bikepoint"
    bikeStations = pd.read_json(url)

    ## Read data on bike trips recursively from all files 
    def idGenerator(x):
        return x.split("_")[1]
    bikeStations.id = np.vectorize(idGenerator)(bikeStations.id)
    bikeStations["demand"] = 0 


    folders =  [x[0] for x in os.walk(os.getcwd() + "/_TfL Cycling Data")]
    folders.pop(0)
    li = []
    for path in folders:
        all_files = glob.glob(path+  "/*.csv")
        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0)
            li.append(df)
        
    trips = pd.concat(li, axis=0, ignore_index=True)


    ## Bike Trip data Wrangling  
    trips[['EndStation Id']] = trips[['EndStation Id']].fillna(value=-1) # Endstations have some empty values, fill with -1 
    trips['EndStation Id'] = trips['EndStation Id'].astype(np.int64)     # Cast as int as empty values default to float 
    trips[['End Date','Start Date']] = trips[['End Date','Start Date']].apply(lambda _: pd.to_datetime(_,format = "%d/%m/%Y %H:%M")) # Convert dates to datetime objects 
    print(trips.shape[0])
    trips  = trips[trips['StartStation Id'].isin(bikeStations.index)]
    trips  = trips[trips['EndStation Id'].isin(bikeStations.index)]
    print(trips.shape[0])
    return trips,bikeStations

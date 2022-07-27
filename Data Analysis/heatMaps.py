import pandas as pd 
import geopandas as gpd
import folium
from folium import plugins
from folium.plugins import MarkerCluster,HeatMap
import math

bikeStationsDaily = pd.read_pickle("bikestationswithdailydemand.pkl")
bikeStationsWeekly = pd.read_pickle("bikestationswithweeklydemand.pkl")

map = folium.Map(location = [51.5073219, -0.1276474], tiles='cartodbdark_matter' , zoom_start = 13 )
#folium.TileLayer('cartodbdark_matter').add_to(map)
fg_supply = folium.FeatureGroup(name = "Supply", show = True)
fg_demand = folium.FeatureGroup(name = "Demand", show = False)
demandList = [] 
supplyList = [] 


for x in bikeStationsDaily.index:
    demand = bikeStationsDaily['demand'][x]
    supply = False
    if demand>0:
        demand = math.floor(demand)
    else:
        demand = abs(math.ceil(demand))
        supply=True
    if supply:
        for _ in range(1,demand +1):
            demandList.append([bikeStationsDaily['lat'][x], bikeStationsDaily['lon'][x]])
          
        
    else:
        for _ in range(1,demand +1):
            supplyList.append([bikeStationsDaily['lat'][x], bikeStationsDaily['lon'][x]])
       



HeatMap(demandList,gradient={.6: 'red', .98: 'red', 1: 'red'}).add_to(fg_demand)
HeatMap(supplyList,gradient={.6: 'green', .98: 'lime', 1: 'green'}).add_to(fg_supply)

fg_demand.add_to(map)
fg_supply.add_to(map)

map.save("dailyHeatMap.html")



map = folium.Map(location = [51.5073219, -0.1276474], tiles='cartodbdark_matter' , zoom_start = 13 )
#folium.TileLayer('cartodbdark_matter').add_to(map)
fg_supply = folium.FeatureGroup(name = "Supply", show = True)
fg_demand = folium.FeatureGroup(name = "Demand", show = False)
demandList = [] 
supplyList = [] 


for x in bikeStationsWeekly.index:
    demand = bikeStationsWeekly['demand'][x]
    supply = False
    if demand>0:
        demand = math.floor(demand)
    else:
        demand = abs(math.ceil(demand))
        supply=True
    if supply:
        for _ in range(1,demand +1):
            demandList.append([bikeStationsWeekly['lat'][x], bikeStationsWeekly['lon'][x]])
          
        
    else:
        for _ in range(1,demand +1):
            supplyList.append([bikeStationsWeekly['lat'][x], bikeStationsWeekly['lon'][x]])
       



HeatMap(demandList,gradient={.6: 'blue', .98: 'red', 1: 'red'}).add_to(fg_demand)
HeatMap(supplyList,gradient={.6: 'blue', .98: 'lime', 1: 'green'}).add_to(fg_supply)

fg_demand.add_to(map)
fg_supply.add_to(map)

map.save("weeklyHeatMap.html")

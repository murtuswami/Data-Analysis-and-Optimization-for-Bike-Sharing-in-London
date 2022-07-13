import folium 
from folium import plugins
from folium.plugins import HeatMap,HeatMapWithTime,MarkerCluster
import math

def mapClusters(bikeStations,title):
   
    map = folium.Map(location = [51.5073219, -0.1276474], tiles='cartodbdark_matter' , zoom_start = 13 )
    #folium.TileLayer('cartodbdark_matter').add_to(map)
    fg_supply = folium.FeatureGroup(name = "Supply", show = True)
    fg_demand = folium.FeatureGroup(name = "Demand", show = False)
    marker_cluster = MarkerCluster().add_to(fg_demand)
    marker_cluster2 = MarkerCluster().add_to(fg_supply)

    for x in bikeStations.index:
        print(bikeStations['lon'][x],bikeStations['lat'][x],bikeStations['demand'][x],bikeStations['id'][x])
        demand = bikeStations['demand'][x]
        supply = False
        if demand>0:
            demand = math.floor(demand)
        else:
            demand = abs(math.ceil(demand))
            supply=True
        if supply:
            for _ in range(1,demand +1):
                folium.Marker(
                location=[bikeStations['lat'][x], bikeStations['lon'][x]],
                popup=bikeStations['demand'][x],
                icon=folium.Icon(color='green', prefix='fa',icon='bicycle')
                ).add_to(marker_cluster2)
            
        else:
            for _ in range(1,demand +1):
                folium.Marker(
                location=[bikeStations['lat'][x], bikeStations['lon'][x]],
                popup=bikeStations['demand'][x],
                icon=folium.Icon(color='red', prefix='fa',icon='bicycle')
                ).add_to(marker_cluster)

    fg_demand.add_to(map)
    fg_supply.add_to(map)
    map.add_child(folium.LayerControl())
    map.save(title+ ".html")
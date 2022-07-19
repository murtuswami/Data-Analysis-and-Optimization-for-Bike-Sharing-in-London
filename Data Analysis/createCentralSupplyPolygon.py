from shapely.geometry import Polygon
import geopandas as gpd

def createPoly():
    lonList = [-0.18,-0.154,-0.148,-0.14,-0.13,-0.109,-0.105,-0.1,-0.09,-0.074,-0.074,-0.078,-0.117,-0.127,-0.14,-0.148,-0.162,-0.174,-0.18]
    latList = [51.5,51.518,51.52,51.521,51.523,51.522,51.524,51.523,51.527,51.524,51.509,51.5,51.497,51.493,51.493,51.492,51.489,51.494,51.495]
    print(len(lonList))
    print(len(latList))
    polygon_geom = Polygon(zip(lonList, latList))
    crs = {'init': 'epsg:4326'}
    polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])       
    return polygon,polygon_geom

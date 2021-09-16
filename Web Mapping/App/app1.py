import pandas as pd
import folium

data = pd.read_csv("Volcanoes.txt", sep= ",")   #No need for the sep arg, I added it just because
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_elev(e):
    if e < 1000:
        return 'green'
    elif 1000 <= e < 3000:
        return 'orange'
    else:
        return 'red'

def give_markers_grp_2():
    Feat_grp = folium.FeatureGroup(name= "Volcanoes Markers")
    for la, lo, na, e in zip(lat, lon, name, elev):
        Feat_grp.add_child(folium.CircleMarker(location= [la,lo], radius= 6, popup= na, fill_color = color_elev(e), color = 'grey', fill_opacity = 0.7))
    return Feat_grp

map_final__promis = folium.Map(location= [40.866667, 34.566667], zoom_control= 6, tiles = "Stamen Terrain")

feature_grp_final1 = give_markers_grp_2()
feature_grp_final12 = folium.FeatureGroup(name = "Population Map")
feature_grp_final12.add_child(folium.GeoJson(data = open("world.json", 'r', encoding= 'utf-8-sig').read(),
style_function = lambda x : {'fillColor' : 'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if x['properties']['POP2005'] < 20000000 else 'red'}))

map_final__promis.add_child(feature_grp_final1)
map_final__promis.add_child(feature_grp_final12)
map_final__promis.add_child(folium.LayerControl())

map_final__promis.save("InteractiveMap.html")
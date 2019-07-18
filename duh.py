import folium
import pandas

data = pandas.read_csv("volcanoes_usa.txt")
lat = list(data['LAT'])
lon = list(data['LON'])
elev = list(data['ELEV'])

map = folium.Map(location=[38.58, -99], zoom_start=5, tiles='Mapbox Bright')

def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"
    

#adding features within groups
fgv = folium.FeatureGroup(name="Volcanoes")
#one way to do it:
    #map.add_child(folium.Marker(location=[38.2, -99.1], popup="Hi, Im a marker", icon=folium.Icon(color='green')));
#second way:
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=str(el) + " m", radius=6, fill_color=color_producer(el), fill_opacity=0.7, color="grey"))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(), 
    style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 1000000 
    else 'orange' if 1000000 <= x['properties']['POP2005'] <= 20000000 else 'red'}))

map.add_child(fgv) #then add the featured group as a child
map.add_child(fgp)
map.add_child(folium.LayerControl()) #looks for objects added to map, only one child and folium will treat this together
map.save('Map1.html')

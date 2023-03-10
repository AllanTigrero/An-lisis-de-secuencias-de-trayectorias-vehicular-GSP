import folium 
import numpy as np
import pandas as pd

datos = pd.read_csv("RomaVelocidad2.csv", sep=",",decimal=".")

rango = 0.0003
datos['lon_minima'] = 12.4836 + (datos['grupo_long']-1) * rango
datos['lon_maxima'] = 12.4836 + (datos['grupo_long']+0) * rango
datos['lat_minima'] = 41.8983 + (datos['grupo_lat']-1) * rango
datos['lat_maxima'] = 41.8983 + (datos['grupo_lat']+0) * rango

# ubicar el punto centrico del mapa
max_lon = datos.lon_maxima.max()
min_lon = datos.lon_minima.min()
max_lat = datos.lat_maxima.max()
min_lat = datos.lat_minima.min()

center_lon = (min_lon + max_lon)/2
center_lat = (min_lat + max_lat)/2

colors = ["white","lightblue","orange","red","green"]
color_labels = ["Secuencias 0", "Secuencias 1", "Secuencias 2", "Secuencias 3", "Secuencias 4", "Secuencias 5", "Secuencias 6", "Secuencias 7", "Secuencias 8", "Secuencias 9", "Secuencias 10", "Secuencias 11", "Secuencias 12", "Secuencias 13", "Secuencias 14", "Secuencias 15"]# Crear el mapa base (mapa interactivo)
mapa = folium.Map(location=[center_lat, center_lon], zoom_start=15)
legend_html = '''
     <div style="position: fixed; 
     background: rgba(255,255,255,0.8); bottom: 50px; left: 50px; width: 150px; height: 150px; 
     border-radius: 5px; solid grey; z-index:9999; font-size:14px;
     ">&nbsp; <b>SECUENCIAS</b><br>
     '''

for color, label in zip(colors, color_labels):
    legend_html += '''
        &nbsp; <span style="background-color:''' + color + ''';
        display:inline-block;width:40px;height:10px;"></span>&nbsp; ''' + label + '''<br>
        '''

legend_html += '''
     </div>
     '''

mapa.get_root().html.add_child(folium.Element(legend_html))

for i in range(len(datos)):
    recB = [(datos['lat_maxima'][i], datos['lon_maxima'][i]), (datos['lat_minima'][i], datos['lon_minima'][i])] 
    folium.Rectangle(
        recB,
        color= colors[datos['support'][i]],
        weight=1,
        fill=True,
        fill_color=colors[datos['support'][i]],
        fill_opacity=0.7
    ).add_to(mapa)

    # Agregar marcador en el centro del rectángulo
    center_lat = (datos['lat_maxima'][i] + datos['lat_minima'][i]) / 2
    center_lon = (datos['lon_maxima'][i] + datos['lon_minima'][i]) / 2
    tooltip = "Click me!"
    folium.Marker(
        [center_lat, center_lon],
        icon=folium.Icon(color=colors[datos['support'][i]]),
        popup="INFORMACION"+"<br> Secuencias: "+str(datos['support'][i])+"<br> Grupo_long: "+str(datos['grupo_long'][i])+"<br> Grupo_lat: "+str(datos['grupo_lat'][i])
        +"<br> Velocidad Promedio: "+str(datos['vel_prom'][i])+"km/h",
        tooltip=tooltip
    ).add_to(mapa)

mapa.save("MapaVelocidadRomaLargo2.html")

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Area dle poligono
poli_area = [
    (14.583336980488415, -90.52132423960929),
    (14.587501398035755, -90.52000762192105),
    (14.5908577369413, -90.5189800178717),
    (14.594541538032592, -90.51666033017163),
    (14.59558270318996, -90.51730585992055),
    (14.601413137017506, -90.51614390637249),
    (14.601496427809725, -90.51820960156904),
    (14.602787431055434, -90.5185969194184),
    (14.604390359806596, -90.5282313081852),
    (14.603336631958895, -90.5281961821182),
    (14.60058331923507, -90.5259832398961),
    (14.595212560669165, -90.52138172511685),
    (14.586454006524356, -90.5236963490549),
    (14.585587329711274, -90.52124571715663),
    (14.583346703378275, -90.52176323888933),
]

# Confi
type_net = 'drive'  

# Centro 
centro = {
    'lat': 14.5935,
    'lon': -90.5220
}
zoomInit = 15

# Confi
API_HOST = "0.0.0.0"
API_PORT = 8000
 
# Rutas de archivos
archNodosCSV = os.path.join(BASE_DIR, "nodos_generados.csv")
archNodosPerson = os.path.join(BASE_DIR, "nodos_personalizados.csv")
archAristasCSV = os.path.join(BASE_DIR, "aristas_generadas.csv")
archAristasPerson = os.path.join(BASE_DIR, "aristas_personalizadas.csv")
archiGrafoCache = os.path.join(BASE_DIR, "grafo_guatemala.graphml")

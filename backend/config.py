import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Area del poligono
poli_area = [
    (14.582679265600747, -90.52070796804428),
    (14.586209528677085, -90.51963508443328),
    (14.593892846756063, -90.51667392566688),
    (14.597547520133299, -90.51581561877808),
    (14.602115776502082, -90.51500022723332),
    (14.603029416385484, -90.51521480395552),
    (14.603901523678099, -90.52126586752063),
    (14.605313499522854, -90.52881896814215),
    (14.603818465993106, -90.52967727503095),
    (14.601492838077473, -90.52723110039786),
    (14.597755170266273, -90.52439868766479),
    (14.59501417351114, -90.52208125906499),
    (14.5899473926521, -90.52332580405375),
    (14.585586545247118, -90.52457034904253),
    (14.585046624797448, -90.52203834372055),
    (14.585129689428621, -90.52186668234908),
    (14.582928462417458, -90.52238166648236),
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
API_PORT = 8002
 
# Rutas de archivos
archNodosCSV = os.path.join(BASE_DIR, "nodos_generados.csv")
archNodosPerson = os.path.join(BASE_DIR, "nodos_personalizados.csv")
archAristasCSV = os.path.join(BASE_DIR, "aristas_generadas.csv")
archAristasPerson = os.path.join(BASE_DIR, "aristas_personalizadas.csv")
archiGrafoCache = os.path.join(BASE_DIR, "grafo_guatemala.graphml")

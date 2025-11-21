import networkx as nx
from graph_manager import GraphManager

class Algorithms:
    def __init__(self):
        self.gm = GraphManager()
        self.grafo = self.gm.cargar_grafo()
        self.gm.cargar_nombres_personalizados()
        self.gm.cargar_aristas_personalizadas()

    def ruta_simple(self, origen, destino):
        try:
            ruta = nx.dijkstra_path(self.grafo, origen, destino, weight='peso')
            distancia = nx.dijkstra_path_length(self.grafo, origen, destino, weight='peso')
            return {'ruta': ruta, 'distancia': distancia}
        except nx.NetworkXNoPath:
            return {'ruta': [], 'distancia': float('inf')}

    def ruta_con_parada(self, origen, parada, destino):
        parte1 = self.ruta_simple(origen, parada)
        parte2 = self.ruta_simple(parada, destino)
        if parte1['ruta'] and parte2['ruta']:
            ruta_total = parte1['ruta'] + parte2['ruta'][1:]
            distancia_total = parte1['distancia'] + parte2['distancia']
            return {'ruta': ruta_total, 'distancia': distancia_total}
        return {'ruta': [], 'distancia': float('inf')}

    def ruta_con_obstaculo(self, origen, destino, obstaculo):
        G_temp = self.grafo.copy()
        if obstaculo in G_temp.nodes:
            G_temp.remove_node(obstaculo)
        try:
            ruta = nx.dijkstra_path(G_temp, origen, destino, weight='peso')
            distancia = nx.dijkstra_path_length(G_temp, origen, destino, weight='peso')
            return {'ruta': ruta, 'distancia': distancia}
        except nx.NetworkXNoPath:
            return {'ruta': [], 'distancia': float('inf')}

    def ruta_con_trafico(self, origen, destino, factor_calles=None, factor_extra=8.0):

        G_temp = self.grafo.copy()

        for u, v, data in G_temp.edges(data=True):
            peso_original = data.get('peso', 0)  

            
            factor_trafico = data.get('factor_trafico', 8.0)

            if factor_calles and data['nombre_calle'] in factor_calles:
                data['peso'] = peso_original * factor_calles[data['nombre_calle']]
            else:
                
                data['peso'] = peso_original * factor_trafico * factor_extra

        try:
            ruta = nx.dijkstra_path(G_temp, origen, destino, weight='peso')
            distancia = nx.dijkstra_path_length(G_temp, origen, destino, weight='peso')
            return {'ruta': ruta, 'distancia': distancia}
        except nx.NetworkXNoPath:
            return {'ruta': [], 'distancia': float('inf')}

import networkx as nx
from graph_manager import GraphManager

class Algorithms:
    def __init__(self, grafo=None):
        if grafo is not None:
            self.grafo = grafo
        else:
            self.gm = GraphManager()
            self.grafo = self.gm.cargar_grafo()
            self.gm.cargar_nombres_personalizados()
            self.gm.cargar_aristas_personalizadas()

    def obtener_pois(self):
        """Devuelve lista de nodos que son POI"""
        if self.grafo is None:
            raise ValueError("Grafo no cargado aún")
        return [n for n, data in self.grafo.nodes(data=True) if data.get("tipo") == "POI"]

    def obtener_info_poi(self, poi_id):
        """Devuelve info de un POI dado su id"""
        if self.grafo is None:
            raise ValueError("Grafo no cargado aún")
        if poi_id in self.grafo:
            data = self.grafo.nodes[poi_id]
            if data.get("tipo") == "POI":
                return {"nombre": data.get("nombre"), "direccion": data.get("direccion")}
        return None

    def ruta_simple(self, origen, destino):
        """Calcula la ruta más corta (por peso 'peso') entre dos nodos"""
        try:
            ruta = nx.dijkstra_path(self.grafo, origen, destino, weight='peso')
            distancia = nx.dijkstra_path_length(self.grafo, origen, destino, weight='peso')
            return {'ruta': ruta, 'distancia': distancia}
        except nx.NetworkXNoPath:
            return {'ruta': [], 'distancia': float('inf')}

    def ruta_con_parada(self, origen, parada, destino):
        """Ruta pasando por un nodo intermedio"""
        parte1 = self.ruta_simple(origen, parada)
        parte2 = self.ruta_simple(parada, destino)
        if parte1['ruta'] and parte2['ruta']:
            ruta_total = parte1['ruta'] + parte2['ruta'][1:]  # evitar repetir el nodo de la parada
            distancia_total = parte1['distancia'] + parte2['distancia']
            return {'ruta': ruta_total, 'distancia': distancia_total}
        return {'ruta': [], 'distancia': float('inf')}

    def ruta_con_obstaculo(self, origen, destino, obstaculo):
        """Calcula ruta evitando un nodo específico y sus nodos de acceso"""
        G_temp = self.grafo.copy()

        nodos_a_eliminar = set()

        if obstaculo in G_temp.nodes:
            nodos_a_eliminar.add(obstaculo)
            data = G_temp.nodes[obstaculo]
            print(f"[EVITAR] Nodo a evitar: {obstaculo}, tipo: {data.get('tipo')}, nombre: {data.get('nombre')}")

            vecinos_nivel1 = list(G_temp.predecessors(obstaculo)) + list(G_temp.successors(obstaculo))
            print(f"[EVITAR] Vecinos nivel 1 del nodo: {vecinos_nivel1}")

            for vecino in vecinos_nivel1:
                vecino_data = G_temp.nodes.get(vecino, {})
                nombre_vecino = vecino_data.get('nombre', '')
                tipo_vecino = vecino_data.get('tipo', '')

                if 'Acceso' in nombre_vecino or 'Nodo_' in nombre_vecino or tipo_vecino == 'acceso':
                    nodos_a_eliminar.add(vecino)
                    print(f"[EVITAR] Agregando nodo de acceso a eliminar: {vecino} ({nombre_vecino})")

                    vecinos_nivel2 = list(G_temp.predecessors(vecino)) + list(G_temp.successors(vecino))
                    for v2 in vecinos_nivel2:
                        v2_data = G_temp.nodes.get(v2, {})
                        nombre_v2 = v2_data.get('nombre', '')
                        if 'Nodo_' in nombre_v2:
                            nodos_a_eliminar.add(v2)
                            print(f"[EVITAR] Agregando nodo intermedio nivel 2: {v2} ({nombre_v2})")

        print(f"[EVITAR] Total nodos a eliminar: {nodos_a_eliminar}")

        for nodo in nodos_a_eliminar:
            if nodo != origen and nodo != destino and nodo in G_temp.nodes:
                G_temp.remove_node(nodo)
                print(f"[EVITAR] Nodo eliminado: {nodo}")

        try:
            ruta = nx.dijkstra_path(G_temp, origen, destino, weight='peso')
            distancia = nx.dijkstra_path_length(G_temp, origen, destino, weight='peso')
            print(f"[EVITAR] Ruta encontrada con {len(ruta)} nodos")
            return {'ruta': ruta, 'distancia': distancia}
        except nx.NetworkXNoPath:
            print("[EVITAR] No se encontró ruta alternativa")
            return {'ruta': [], 'distancia': float('inf')}

    def ruta_con_trafico(self, origen, destino, factor_calles=None, factor_extra=3.0):
        """Calcula ruta considerando tráfico; factor_calles es dict nombre_calle -> multiplicador"""
        G_temp = self.grafo.copy()
        for u, v, data in G_temp.edges(data=True):
            peso_original = data.get('peso', 0)
            factor_trafico = data.get('factor_trafico', 3.0)
            if factor_calles and data.get('nombre_calle') in factor_calles:
                data['peso'] = peso_original * factor_calles[data['nombre_calle']]
            else:
                data['peso'] = peso_original * factor_trafico * factor_extra
        try:
            ruta = nx.dijkstra_path(G_temp, origen, destino, weight='peso')
            distancia = nx.dijkstra_path_length(G_temp, origen, destino, weight='peso')
            return {'ruta': ruta, 'distancia': distancia}
        except nx.NetworkXNoPath:
            return {'ruta': [], 'distancia': float('inf')}

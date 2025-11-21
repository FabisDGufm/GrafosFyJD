import osmnx as ox
import networkx as nx
import pandas as pd
from shapely.geometry import Polygon
from config import poli_area, type_net, archNodosCSV, archNodosPerson, archAristasCSV, archAristasPerson

class GraphManager:
    def __init__(self):
        self.grafo = None

    def cargar_grafo(self):
        poligono = Polygon([(lon, lat) for lat, lon in poli_area])
        self.grafo = ox.graph_from_polygon(poligono, network_type=type_net)
        print(f"Grafo cargado: {self.grafo.number_of_nodes()} nodos, {self.grafo.number_of_edges()} aristas")
        return self.grafo

    def exportar_nodos_csv(self):
        if self.grafo is None:
            self.cargar_grafo()

        nodos = []
        for i, (node_id, data) in enumerate(self.grafo.nodes(data=True)):
            nodos.append({
                'id': node_id,
                'lat': data['y'],
                'lon': data['x'],
                'nombre': f'Interseccion_{i+1}',
                'tipo': 'interseccion',
                'street_count': data.get('street_count', 0)
            })

        df = pd.DataFrame(nodos)
        df.to_csv(archNodosCSV, index=False)
        print(f"CSV generado: {archNodosCSV} con {len(nodos)} nodos")
        return df

    def cargar_nombres_personalizados(self):
        if self.grafo is None:
            self.cargar_grafo()

        try:
            df = pd.read_csv(archNodosPerson)
            for _, row in df.iterrows():
                node_id = row['id']
                if node_id in self.grafo.nodes:
                    self.grafo.nodes[node_id]['nombre'] = row['nombre']
                    if 'tipo' in row:
                        self.grafo.nodes[node_id]['tipo'] = row['tipo']
            print(f"Nombres personalizados cargados desde {archNodosPerson}")
        except FileNotFoundError:
            print(f"Archivo {archNodosPerson} no encontrado, usando nombres por defecto")

    def obtener_nodo_cercano(self, lat, lon):
        return ox.distance.nearest_nodes(self.grafo, lon, lat)

    def obtener_info_nodo(self, node_id):
        if node_id in self.grafo.nodes:
            data = self.grafo.nodes[node_id]
            return {
                'id': node_id,
                'lat': data['y'],
                'lon': data['x'],
                'nombre': data.get('nombre', f'Nodo_{node_id}'),
                'tipo': data.get('tipo', 'interseccion')
            }
        return None

    def obtener_todos_los_nodos(self):
        nodos = []
        for node_id, data in self.grafo.nodes(data=True):
            nodos.append({
                'id': node_id,
                'lat': data['y'],
                'lon': data['x'],
                'nombre': data.get('nombre', f'Nodo_{node_id}')
            })
        return nodos

    def obtener_todas_las_aristas(self):
        aristas = []
        for u, v, data in self.grafo.edges(data=True):
            aristas.append({
                'origen': u,
                'destino': v,
                'nombre': data.get('name', 'Sin nombre'),
                'distancia': data.get('length', 0),
                'coords': [
                    [self.grafo.nodes[u]['y'], self.grafo.nodes[u]['x']],
                    [self.grafo.nodes[v]['y'], self.grafo.nodes[v]['x']]
                ]
            })
        return aristas

    def exportar_aristas_csv(self):
        if self.grafo is None:
            self.cargar_grafo()

        aristas = []
        for u, v, data in self.grafo.edges(data=True):
            lat_o, lon_o = self.grafo.nodes[u]['y'], self.grafo.nodes[u]['x']
            lat_d, lon_d = self.grafo.nodes[v]['y'], self.grafo.nodes[v]['x']

            # Calcular direccion aproximada
            if lat_d > lat_o:
                dir_ns = 'norte'
            elif lat_d < lat_o:
                dir_ns = 'sur'
            else:
                dir_ns = ''

            if lon_d > lon_o:
                dir_ew = 'este'
            elif lon_d < lon_o:
                dir_ew = 'oeste'
            else:
                dir_ew = ''

            direccion = f"{dir_ns}-{dir_ew}" if dir_ns and dir_ew else (dir_ns or dir_ew or 'mismo punto')

            aristas.append({
                'origen': u,
                'destino': v,
                'nombre_calle': data.get('name', 'Sin nombre'),
                'distancia': round(data.get('length', 0), 2),
                'direccion': direccion,
                'factor_trafico': 1.0
            })

        df = pd.DataFrame(aristas)
        df.to_csv(archAristasCSV, index=False)
        print(f"CSV generado: {archAristasCSV} con {len(aristas)} aristas")
        return df

    def cargar_aristas_personalizadas(self):
        if self.grafo is None:
            self.cargar_grafo()

        try:
            df = pd.read_csv(archAristasPerson)
            for _, row in df.iterrows():
                u, v = row['origen'], row['destino']
                if self.grafo.has_edge(u, v):
                    factor = row.get('factor_trafico', 1.0)
                    dist = self.grafo[u][v][0]['length']
                    self.grafo[u][v][0]['peso'] = dist * factor
            print(f"Pesos personalizados cargados desde {archAristasPerson}")
        except FileNotFoundError:
            print(f"Archivo {archAristasPerson} no encontrado, usando pesos por defecto")


if __name__ == "__main__":
    gm = GraphManager()
    gm.cargar_grafo()
    gm.exportar_nodos_csv()
    gm.exportar_aristas_csv()
    print("\nListo! Edita los CSV y renombralos a 'nodos_personalizados.csv' y 'aristas_personalizadas.csv'")


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from algorithms import Algorithms
from config import API_HOST, API_PORT

app = FastAPI(title="No Waze API", description="API para navegacion en Guatemala City")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

algo = None

def get_algo():
    global algo
    if algo is None:
        print("Cargando grafo...")
        algo = Algorithms()
        print("Grafo listo")
    return algo

class RutaDirectaRequest(BaseModel):
    origen: str
    destino: str

class RutaViaRequest(BaseModel):
    origen: str
    waypoint: str
    destino: str

class RutaEvitarRequest(BaseModel):
    origen: str
    destino: str
    evitar: str

@app.get("/")
def root():
    return {"status": "ok", "message": "No Waze API"}

@app.get("/api/nodos")
def get_nodos():
    algorithms = get_algo()
    nodos = []
    for node_id, data in algorithms.grafo.nodes(data=True):
        nodos.append({
            "id": str(node_id),
            "lat": data.get("y"),
            "lon": data.get("x"),
            "nombre": data.get("nombre", f"Nodo_{node_id}"),
            "tipo": data.get("tipo", "calle"),
            "direccion": data.get("direccion", "")
        })
    return nodos

@app.get("/api/pois")
def get_pois():
    algorithms = get_algo()
    pois = []
    for node_id in algorithms.obtener_pois():
        data = algorithms.grafo.nodes[node_id]
        pois.append({
            "id": str(node_id),
            "lat": data.get("y"),
            "lon": data.get("x"),
            "nombre": data.get("nombre"),
            "tipo": "POI",
            "direccion": data.get("direccion", "")
        })
    return pois

@app.get("/api/aristas")
def get_aristas():
    algorithms = get_algo()
    aristas = []
    for u, v, data in algorithms.grafo.edges(data=True):
        u_data = algorithms.grafo.nodes[u]
        v_data = algorithms.grafo.nodes[v]
        aristas.append({
            "origen": str(u),
            "destino": str(v),
            "nombre_calle": data.get("name", "Sin nombre"),
            "distancia": data.get("length", 0),
            "coords": [
                [u_data.get("y"), u_data.get("x")],
                [v_data.get("y"), v_data.get("x")]
            ]
        })
    return aristas

@app.get("/api/grafo/info")
def get_grafo_info():
    algorithms = get_algo()
    return {
        "nodos": algorithms.grafo.number_of_nodes(),
        "aristas": algorithms.grafo.number_of_edges(),
        "pois": len(algorithms.obtener_pois())
    }

@app.post("/api/ruta/directa")
def ruta_directa(req: RutaDirectaRequest):
    algorithms = get_algo()
    try:
        origen_id = int(req.origen)
        destino_id = int(req.destino)
    except ValueError:
        return {"error": "IDs invalidos"}

    resultado = algorithms.ruta_simple(origen_id, destino_id)

    if not resultado["ruta"]:
        return {"error": "No se encontro ruta", "coords": [], "distancia": 0}

    coords = []
    for node_id in resultado["ruta"]:
        data = algorithms.grafo.nodes[node_id]
        coords.append([data.get("y"), data.get("x")])

    return {
        "coords": coords,
        "distancia": resultado["distancia"],
        "nodos": len(resultado["ruta"]),
        "aristas": len(resultado["ruta"]) - 1,
        "ruta_ids": [str(n) for n in resultado["ruta"]]
    }

@app.post("/api/ruta/via")
def ruta_via(req: RutaViaRequest):
    algorithms = get_algo()
    try:
        origen_id = int(req.origen)
        waypoint_id = int(req.waypoint)
        destino_id = int(req.destino)
    except ValueError:
        return {"error": "IDs invalidos"}

    resultado = algorithms.ruta_con_parada(origen_id, waypoint_id, destino_id)

    if not resultado["ruta"]:
        return {"error": "No se encontro ruta", "coords": [], "distancia": 0}

    coords = []
    for node_id in resultado["ruta"]:
        data = algorithms.grafo.nodes[node_id]
        coords.append([data.get("y"), data.get("x")])

    return {
        "coords": coords,
        "distancia": resultado["distancia"],
        "nodos": len(resultado["ruta"]),
        "aristas": len(resultado["ruta"]) - 1,
        "ruta_ids": [str(n) for n in resultado["ruta"]]
    }

@app.post("/api/ruta/evitar")
def ruta_evitar(req: RutaEvitarRequest):
    algorithms = get_algo()
    try:
        origen_id = int(req.origen)
        destino_id = int(req.destino)
        evitar_id = int(req.evitar)
    except ValueError:
        return {"error": "IDs invalidos"}

    resultado = algorithms.ruta_con_obstaculo(origen_id, destino_id, evitar_id)

    if not resultado["ruta"]:
        return {"error": "No se encontro ruta", "coords": [], "distancia": 0}

    coords = []
    for node_id in resultado["ruta"]:
        data = algorithms.grafo.nodes[node_id]
        coords.append([data.get("y"), data.get("x")])

    return {
        "coords": coords,
        "distancia": resultado["distancia"],
        "nodos": len(resultado["ruta"]),
        "aristas": len(resultado["ruta"]) - 1,
        "ruta_ids": [str(n) for n in resultado["ruta"]]
    }

if __name__ == "__main__":
    import uvicorn
    print(f"Iniciando servidor en http://{API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)

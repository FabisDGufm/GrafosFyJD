const API_URL = 'http://localhost:8000';

async function getNodos() {
    try {
        const response = await fetch(`${API_URL}/api/nodos`);
        return await response.json();
    } catch (error) {
        console.error('Error obteniendo nodos:', error);
        return [];
    }
}

async function getPOIs() {
    try {
        const response = await fetch(`${API_URL}/api/pois`);
        return await response.json();
    } catch (error) {
        console.error('Error obteniendo POIs:', error);
        return [];
    }
}

async function getAristas() {
    try {
        const response = await fetch(`${API_URL}/api/aristas`);
        return await response.json();
    } catch (error) {
        console.error('Error obteniendo aristas:', error);
        return [];
    }
}

async function calcularRutaDirecta(origen, destino) {
    try {
        const response = await fetch(`${API_URL}/api/ruta/directa`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ origen, destino })
        });
        return await response.json();
    } catch (error) {
        console.error('Error calculando ruta directa:', error);
        return null;
    }
}

async function calcularRutaVia(origen, waypoint, destino) {
    try {
        const response = await fetch(`${API_URL}/api/ruta/via`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ origen, waypoint, destino })
        });
        return await response.json();
    } catch (error) {
        console.error('Error calculando ruta via:', error);
        return null;
    }
}

async function calcularRutaEvitando(origen, destino, evitar) {
    try {
        const response = await fetch(`${API_URL}/api/ruta/evitar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ origen, destino, evitar })
        });
        return await response.json();
    } catch (error) {
        console.error('Error calculando ruta evitando:', error);
        return null;
    }
}

async function getGrafoInfo() {
    try {
        const response = await fetch(`${API_URL}/api/grafo/info`);
        return await response.json();
    } catch (error) {
        console.error('Error obteniendo info del grafo:', error);
        return null;
    }
}

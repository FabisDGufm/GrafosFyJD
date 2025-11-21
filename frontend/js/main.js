let nodos = [];
let pois = [];
let aristas = [];
let routeType = 'directa';

document.addEventListener('DOMContentLoaded', async () => {
    initMap();
    await cargarDatos();
});

async function cargarDatos() {
    try {
        nodos = await getNodos();
        console.log(`Cargados ${nodos.length} nodos`);

        if (nodos.length === 0) {
            console.log('API no disponible, usando datos de prueba');
            usarDatosPrueba();
            return;
        }

        pois = nodos.filter(n => n.tipo === 'POI');
        console.log(`Encontrados ${pois.length} POIs`);

        aristas = await getAristas();
        console.log(`Cargadas ${aristas.length} aristas`);

        poblarSelectores();
        mostrarListaPOIs();
        dibujarCalles(aristas);
        dibujarNodos(nodos);
        dibujarPOIs(pois);

    } catch (error) {
        console.error('Error cargando datos:', error);
        usarDatosPrueba();
    }
}

function usarDatosPrueba() {
    pois = [
        { id: '14206194901', nombre: 'Parque 14', lat: 14.588834, lon: -90.519685, tipo: 'POI', direccion: 'Avenida Las Americas' },
        { id: '14206194902', nombre: 'Pollo Campero Las Americas', lat: 14.588239, lon: -90.520363, tipo: 'POI', direccion: 'Avenida Las Americas' },
        { id: '14206194903', nombre: 'Plaza Obelisco', lat: 14.594599, lon: -90.517730, tipo: 'POI', direccion: 'Plaza Obelisco' },
        { id: '14206194904', nombre: 'Plaza Espana', lat: 14.601261, lon: -90.518850, tipo: 'POI', direccion: 'Plaza Espana' },
        { id: '14206194905', nombre: 'CC Montufar', lat: 14.603789, lon: -90.525470, tipo: 'POI', direccion: '11 Calle, Canton Tivoli' },
        { id: '14206194906', nombre: 'McDonalds Blvd Liberacion', lat: 14.599630, lon: -90.524852, tipo: 'POI', direccion: 'Boulevard Liberacion' },
        { id: '14206194907', nombre: 'Shell Aeropuerto', lat: 14.598758, lon: -90.524153, tipo: 'POI', direccion: 'Boulevard Liberacion' },
        { id: '14206194908', nombre: 'Reloj de Flores', lat: 14.596072, lon: -90.521611, tipo: 'POI', direccion: '6a Avenida' },
        { id: '14206194909', nombre: 'Hospital Liberacion', lat: 14.594438, lon: -90.520265, tipo: 'POI', direccion: '15 Avenida' },
        { id: '14206194910', nombre: 'SIB Superintendencia de Bancos', lat: 14.589571, lon: -90.521558, tipo: 'POI', direccion: '7a Calle A' }
    ];

    nodos = [...pois];
    poblarSelectores();
    mostrarListaPOIs();
    dibujarPOIs(pois);
}

function poblarSelectores() {
    const selectOrigen = document.getElementById('origen');
    const selectDestino = document.getElementById('destino');
    const selectWaypoint = document.getElementById('waypoint');

    selectOrigen.innerHTML = '<option value="">Selecciona origen...</option>';
    selectDestino.innerHTML = '<option value="">Selecciona destino...</option>';
    selectWaypoint.innerHTML = '<option value="">Selecciona punto...</option>';

    pois.forEach(poi => {
        const optOrigen = document.createElement('option');
        optOrigen.value = poi.id;
        optOrigen.textContent = poi.nombre;
        selectOrigen.appendChild(optOrigen);

        const optDestino = document.createElement('option');
        optDestino.value = poi.id;
        optDestino.textContent = poi.nombre;
        selectDestino.appendChild(optDestino);

        const optWaypoint = document.createElement('option');
        optWaypoint.value = poi.id;
        optWaypoint.textContent = poi.nombre;
        selectWaypoint.appendChild(optWaypoint);
    });
}

function mostrarListaPOIs() {
    const poiList = document.getElementById('poiList');
    poiList.innerHTML = '';

    pois.forEach(poi => {
        const poiItem = document.createElement('div');
        poiItem.className = 'poi-item';
        poiItem.onclick = () => focusPOI(poi);

        poiItem.innerHTML = `
            <div class="poi-icon">
                <i class="fas fa-star"></i>
            </div>
            <div class="poi-info">
                <div class="poi-name">${poi.nombre}</div>
                <div class="poi-address">${poi.direccion || ''}</div>
            </div>
        `;

        poiList.appendChild(poiItem);
    });
}

function focusPOI(poi) {
    map.setView([poi.lat, poi.lon], 17);
}

function setRouteType(type) {
    routeType = type;

    document.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.type === type) {
            btn.classList.add('active');
        }
    });

    const waypointGroup = document.getElementById('waypointGroup');
    const connector2 = document.getElementById('connector2');

    if (type === 'via' || type === 'evitar') {
        waypointGroup.style.display = 'flex';
        connector2.style.display = 'block';
    } else {
        waypointGroup.style.display = 'none';
        connector2.style.display = 'none';
    }
}

function removeWaypoint() {
    document.getElementById('waypoint').value = '';
    setRouteType('directa');
}

async function calcularRuta() {
    const origen = document.getElementById('origen').value;
    const destino = document.getElementById('destino').value;
    const waypoint = document.getElementById('waypoint').value;
    const usarTrafico = document.getElementById('traficoCheckbox').checked;

    if (!origen || !destino) {
        alert('Por favor selecciona origen y destino');
        return;
    }

    let ruta;
    let colorRuta;

    try {
        // Si trafico esta activado y es ruta directa, usar endpoint de trafico
        if (usarTrafico && routeType === 'directa') {
            ruta = await calcularRutaTrafico(origen, destino);
            colorRuta = '#e74c3c'; // Rojo para indicar trafico
        } else {
            switch (routeType) {
                case 'directa':
                    ruta = await calcularRutaDirecta(origen, destino);
                    colorRuta = '#c9a227';
                    break;

                case 'via':
                    if (!waypoint) {
                        alert('Por favor selecciona un punto intermedio');
                        return;
                    }
                    ruta = await calcularRutaVia(origen, waypoint, destino);
                    colorRuta = '#5a7cb0';
                    break;

                case 'evitar':
                    if (!waypoint) {
                        alert('Por favor selecciona un punto a evitar');
                        return;
                    }
                    ruta = await calcularRutaEvitando(origen, destino, waypoint);
                    colorRuta = '#FF9800';
                    break;
            }
        }

        if (ruta && ruta.coords) {
            dibujarRuta(ruta, colorRuta);
            mostrarResultados(ruta, usarTrafico);
        } else {
            alert('No se pudo calcular la ruta');
        }

    } catch (error) {
        console.error('Error calculando ruta:', error);
        simularRuta();
    }
}

function simularRuta() {
    const origen = document.getElementById('origen').value;
    const destino = document.getElementById('destino').value;

    const origenPoi = pois.find(p => p.id === origen);
    const destinoPoi = pois.find(p => p.id === destino);

    if (origenPoi && destinoPoi) {
        const rutaSimulada = {
            coords: [
                [origenPoi.lat, origenPoi.lon],
                [(origenPoi.lat + destinoPoi.lat) / 2, (origenPoi.lon + destinoPoi.lon) / 2],
                [destinoPoi.lat, destinoPoi.lon]
            ],
            distancia: calcularDistancia(origenPoi.lat, origenPoi.lon, destinoPoi.lat, destinoPoi.lon),
            tiempo: 5,
            nodos: 3
        };

        const colores = { directa: '#4CAF50', via: '#2196F3', evitar: '#FF9800' };
        dibujarRuta(rutaSimulada, colores[routeType]);
        mostrarResultados(rutaSimulada);
    }
}

function calcularDistancia(lat1, lon1, lat2, lon2) {
    const R = 6371000;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

function mostrarResultados(ruta, conTrafico = false) {
    const container = document.getElementById('resultsContainer');
    const content = document.getElementById('resultsContent');

    const tipoTexto = {
        directa: conTrafico ? 'Ruta con Trafico' : 'Ruta Directa',
        via: 'Ruta via Punto',
        evitar: 'Ruta Alternativa'
    };

    const tipoIcono = {
        directa: conTrafico ? 'fa-car' : 'fa-arrows-alt-h',
        via: 'fa-exchange-alt',
        evitar: 'fa-ban'
    };

    content.innerHTML = `
        <div class="result-card ${routeType}">
            <h4>
                <i class="fas ${tipoIcono[routeType]}"></i>
                ${tipoTexto[routeType]}
            </h4>
            <div class="result-stats">
                <div class="stat-item">
                    <i class="fas fa-road"></i>
                    <div>
                        <div class="stat-value">${(ruta.distancia / 1000).toFixed(2)} km</div>
                        <div class="stat-label">Distancia</div>
                    </div>
                </div>
                <div class="stat-item">
                    <i class="fas fa-clock"></i>
                    <div>
                        <div class="stat-value">${ruta.tiempo || Math.ceil(ruta.distancia / 400)} min</div>
                        <div class="stat-label">Tiempo est.</div>
                    </div>
                </div>
                <div class="stat-item">
                    <i class="fas fa-map-pin"></i>
                    <div>
                        <div class="stat-value">${ruta.nodos || ruta.coords.length}</div>
                        <div class="stat-label">Nodos</div>
                    </div>
                </div>
                <div class="stat-item">
                    <i class="fas fa-route"></i>
                    <div>
                        <div class="stat-value">${ruta.aristas || ruta.coords.length - 1}</div>
                        <div class="stat-label">Aristas</div>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.style.display = 'block';
}

function closeResults() {
    document.getElementById('resultsContainer').style.display = 'none';
}

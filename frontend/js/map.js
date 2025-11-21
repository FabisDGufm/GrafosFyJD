const MAP_CENTER = [14.5935, -90.5220];
const MAP_ZOOM = 15;

let map;
let markersLayer;
let routeLayer;
let streetsLayer;
let nodesLayer;
let poisVisible = true;
let streetsVisible = true;
let nodesVisible = true;

function initMap() {
    map = L.map('map').setView(MAP_CENTER, MAP_ZOOM);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap &copy; CARTO',
        maxZoom: 19
    }).addTo(map);

    streetsLayer = L.layerGroup().addTo(map);
    nodesLayer = L.layerGroup().addTo(map);
    markersLayer = L.layerGroup().addTo(map);
    routeLayer = L.layerGroup().addTo(map);
}

function dibujarCalles(aristas) {
    streetsLayer.clearLayers();

    aristas.forEach(arista => {
        const coords = arista.coords;
        if (coords && coords.length === 2) {
            const polyline = L.polyline(coords, {
                color: '#4a4a6a',
                weight: 3,
                opacity: 0.7
            });

            polyline.on('mouseover', function() {
                this.setStyle({ weight: 5, color: '#c9a227' });
            });
            polyline.on('mouseout', function() {
                this.setStyle({ weight: 3, color: '#4a4a6a' });
            });

            polyline.bindPopup(`
                <div class="popup-content">
                    <h4>${arista.nombre_calle || 'Sin nombre'}</h4>
                    <p><strong>Origen ID:</strong> ${arista.origen}</p>
                    <p><strong>Destino ID:</strong> ${arista.destino}</p>
                    <p><strong>Distancia:</strong> ${arista.distancia.toFixed(1)} m</p>
                </div>
            `);

            streetsLayer.addLayer(polyline);
        }
    });
}

function dibujarNodos(nodos) {
    nodesLayer.clearLayers();

    const intersecciones = nodos.filter(n => n.tipo === 'calle');

    intersecciones.forEach(nodo => {
        const circle = L.circleMarker([nodo.lat, nodo.lon], {
            radius: 3,
            fillColor: '#8a8aaa',
            color: '#6a6a8a',
            weight: 1,
            opacity: 0.6,
            fillOpacity: 0.5
        });

        circle.bindPopup(`
            <div class="popup-content">
                <h4>Interseccion</h4>
                <p>ID: ${nodo.id}</p>
                <p>${nodo.direccion || 'Sin nombre'}</p>
            </div>
        `);

        nodesLayer.addLayer(circle);
    });
}

function dibujarPOIs(pois) {
    markersLayer.clearLayers();

    pois.forEach(poi => {
        const icon = L.divIcon({
            className: 'custom-poi-marker',
            html: `<div class="poi-marker-container">
                <div class="poi-marker">
                    <i class="fas fa-star"></i>
                </div>
                <div class="poi-label">${poi.nombre}</div>
            </div>`,
            iconSize: [120, 50],
            iconAnchor: [60, 40]
        });

        const marker = L.marker([poi.lat, poi.lon], { icon });

        marker.bindPopup(`
            <div class="popup-content">
                <h4>${poi.nombre}</h4>
                <p>${poi.direccion || ''}</p>
                <button onclick="setAsOrigin('${poi.id}')" class="popup-btn">
                    <i class="fas fa-play"></i> Origen
                </button>
                <button onclick="setAsDestination('${poi.id}')" class="popup-btn">
                    <i class="fas fa-flag-checkered"></i> Destino
                </button>
            </div>
        `);

        markersLayer.addLayer(marker);
    });

    if (!document.getElementById('poi-marker-styles')) {
        const style = document.createElement('style');
        style.id = 'poi-marker-styles';
        style.textContent = `
            .poi-marker-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                pointer-events: none;
            }
            .poi-marker {
                width: 26px;
                height: 26px;
                background: #c9a227;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #1a2744;
                font-size: 10px;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
                border: 2px solid white;
                pointer-events: auto;
                cursor: pointer;
            }
            .poi-label {
                background: #1a2744;
                color: white;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 9px;
                font-weight: 400;
                white-space: nowrap;
                margin-top: 4px;
                max-width: 100px;
                overflow: hidden;
                text-overflow: ellipsis;
                text-align: center;
                pointer-events: auto;
                box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            }
            .popup-content h4 {
                margin: 0 0 8px 0;
                color: #1a2744;
            }
            .popup-content p {
                margin: 0 0 12px 0;
                color: #5f6368;
                font-size: 12px;
            }
            .popup-btn {
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
                background: #c9a227;
                color: #1a2744;
                font-size: 11px;
                font-weight: 500;
                cursor: pointer;
                margin-right: 4px;
            }
            .popup-btn:hover {
                background: #d4ad32;
            }
        `;
        document.head.appendChild(style);
    }
}

function dibujarRuta(ruta, color = '#4CAF50', clearPrevious = true) {
    if (clearPrevious) {
        routeLayer.clearLayers();
    }

    if (!ruta || !ruta.coords || ruta.coords.length === 0) {
        console.error('Ruta invalida');
        return;
    }

    const polyline = L.polyline(ruta.coords, {
        color: color,
        weight: 6,
        opacity: 0.9,
        lineCap: 'round',
        lineJoin: 'round'
    });

    routeLayer.addLayer(polyline);

    const startIcon = L.divIcon({
        className: 'route-marker-start',
        html: '<div style="width:20px;height:20px;background:#4CAF50;border-radius:50%;border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    });
    L.marker(ruta.coords[0], { icon: startIcon }).addTo(routeLayer);

    const endIcon = L.divIcon({
        className: 'route-marker-end',
        html: '<div style="width:20px;height:20px;background:#f44336;border-radius:50%;border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    });
    L.marker(ruta.coords[ruta.coords.length - 1], { icon: endIcon }).addTo(routeLayer);

    map.fitBounds(polyline.getBounds(), { padding: [50, 50] });
}

function dibujarWaypoint(lat, lon) {
    const waypointIcon = L.divIcon({
        className: 'route-marker-waypoint',
        html: '<div style="width:16px;height:16px;background:#FF9800;border-radius:50%;border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);"></div>',
        iconSize: [16, 16],
        iconAnchor: [8, 8]
    });
    L.marker([lat, lon], { icon: waypointIcon }).addTo(routeLayer);
}

function clearRoute() {
    routeLayer.clearLayers();
    document.getElementById('resultsContainer').style.display = 'none';
}

function centerMap() {
    map.setView(MAP_CENTER, MAP_ZOOM);
}

function togglePOIs() {
    poisVisible = !poisVisible;
    if (poisVisible) {
        map.addLayer(markersLayer);
    } else {
        map.removeLayer(markersLayer);
    }
}

function toggleStreets() {
    streetsVisible = !streetsVisible;
    if (streetsVisible) {
        map.addLayer(streetsLayer);
    } else {
        map.removeLayer(streetsLayer);
    }
}

function setAsOrigin(id) {
    document.getElementById('origen').value = id;
    map.closePopup();
}

function setAsDestination(id) {
    document.getElementById('destino').value = id;
    map.closePopup();
}

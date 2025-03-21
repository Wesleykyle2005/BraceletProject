// Inicializar el mapa
var map = L.map('map').setView([0, 0], 2);

// Añadir capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Definir un ícono personalizado
var customIcon = L.icon({
    iconUrl: '/static/stores/images/custom-marker.png',
    iconSize: [60, 60],
    iconAnchor: [30, 60],
    popupAnchor: [0, -60]
});

// Añadir marcadores de tiendas
var stores = JSON.parse(document.getElementById('store-data').textContent);
console.log(stores);

stores.forEach(function(store) {
    var marker = L.marker([store.lat, store.lng], { icon: customIcon }).addTo(map);
    marker.bindPopup(
        `<div style="color: black;">
            <b>${store.name}</b><br>${store.description}<br>
            <a href="${store.url}" class="btn btn-primary btn-sm mt-2">Ver productos</a>
        </div>`
    );
    console.log(store);
});

// Ajustar el mapa para mostrar todos los marcadores
var bounds = L.latLngBounds(stores.map(store => [store.lat, store.lng]));
map.fitBounds(bounds);

// Añadir marcador por defecto con popup activo
var defaultMarker = L.marker([12.1319899, -86.2698851]).addTo(map);
defaultMarker.bindPopup(
    `<div style="color: white;">
        <b>Ubicación actual</b><br>Usted está aquí.
    </div>`
).openPopup(); // Abrir popup por defecto

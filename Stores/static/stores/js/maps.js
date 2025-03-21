// Inicializar el mapa
var map = L.map('map').setView([0, 0], 2); // Coordenadas iniciales y zoom

// Añadir capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Definir un ícono personalizado
var customIcon = L.icon({
    iconUrl: '/static/stores/images/custom-marker.png', // Ruta al ícono personalizado
    iconSize: [60, 60], // Tamaño del ícono
    iconAnchor: [30, 60], // Punto del ícono que se posicionará en las coordenadas
    popupAnchor: [0, -60] // Punto desde donde se abrirá el popup
});

// Añadir marcadores de tiendas
var stores = JSON.parse(document.getElementById('store-data').textContent);
console.log(stores);

stores.forEach(function(store) {
    var marker = L.marker([store.lat, store.lng], { icon: customIcon }).addTo(map); // Usar el ícono personalizado
    marker.bindPopup(
        `<b>${store.name}</b><br>${store.description}<br><a href="${store.url}" class="btn btn-primary btn-sm mt-2">Ver productos</a>`
    );
    console.log(store);
});

// Ajustar el mapa para mostrar todos los marcadores
var bounds = L.latLngBounds(stores.map(store => [store.lat, store.lng]));
map.fitBounds(bounds);
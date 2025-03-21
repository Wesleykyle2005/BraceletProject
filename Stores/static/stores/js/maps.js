// Inicializar el mapa
var map = L.map('map').setView([0, 0], 2); // Coordenadas iniciales y zoom

// Añadir capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Añadir marcadores de tiendas
var stores = JSON.parse(document.getElementById('store-data').textContent);
console.log(stores);

stores.forEach(function(store) {
    var marker = L.marker([store.lat, store.lng]).addTo(map);
    marker.bindPopup("<b>" + store.name + "</b><br>" + store.description + "<br><a href='" + store.url + "'>Ver productos</a>");
    console.log(store);
});

// Ajustar el mapa para mostrar todos los marcadores
var bounds = L.latLngBounds(stores.map(store => [store.lat, store.lng]));
map.fitBounds(bounds);
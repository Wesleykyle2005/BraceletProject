import os
import django
import requests
from decimal import Decimal

# Configurar la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BraceletProject.settings')

# Inicializar Django
django.setup()

from products.models import Product, Category
from Stores.models import Store

def fetch_and_store_products():
    url = "https://api.escuelajs.co/api/v1/products"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al obtener los datos de la API.")
        return

    data = response.json()
    # Limitar a los primeros 50 productos
    products_data = data[:50]

    # Coordenadas para las tiendas
    coordinates = [
        (12.128739308961103, -86.26881181418183),
        (12.128131784720749, -86.27047205843127),
        (12.131625812854407, -86.27171792917214),
        (12.133083543826517, -86.26809182800397),
        (12.134209577515016, -86.2725273932548),
    ]

    store_count = 0
    current_store = None

    for index, item in enumerate(products_data):
        # Crear una nueva tienda cada 10 productos
        if index % 10 == 0:
            coord = coordinates[store_count % len(coordinates)]
            current_store = Store.objects.create(
                name=f"Tienda {store_count + 1}",
                description=f"Descripción de la Tienda {store_count + 1}",
                address=f"Dirección de la Tienda {store_count + 1}",
                latitude=Decimal(coord[0]),
                longitude=Decimal(coord[1]),
                phone=f"+505 8888 000{store_count + 1}",
                email=f"tienda{store_count + 1}@example.com",
                image_url="https://via.placeholder.com/150",
                rating=5,
                active=True
            )
            store_count += 1

        # Crear o actualizar el producto
        name = item.get('title', 'Producto sin título')
        price = item.get('price', 0)
        description = item.get('description', '')
        images = item.get('images', [])
        image_url = images[0] if images else ""

        product, created = Product.objects.update_or_create(
            name=name,
            defaults={
                'price': price,
                'description': description,
                'image_url': image_url,
                'available': True,
                'available_units': 10,
                'store': current_store  # Relacionar con la tienda actual
            }
        )

        # Manejo de categoría (opcional)
        if item.get('category'):
            cat_name = item['category'].get('name', 'Categoría desconocida')
            category_obj, _ = Category.objects.get_or_create(name=cat_name)
            product.categories.set([category_obj])

    print("Datos importados o actualizados correctamente.")

# Ejecutar la función principal
if __name__ == "__main__":
    fetch_and_store_products()
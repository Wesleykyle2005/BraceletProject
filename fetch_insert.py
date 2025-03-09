import os
import django
import requests

# Configurar la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BraceletProject.settings')

# Inicializar Django
django.setup()

from products.models import Product, Category

def fetch_and_store_products():
    url = "https://api.escuelajs.co/api/v1/products"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al obtener los datos de la API.")
        return

    data = response.json()
    # Limitar a los primeros 50 productos
    products_data = data[:50]

    for item in products_data:
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
                'available_units': 10
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
import os
import django

# Configurar la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BraceletProject.settings')

# Configurar Django
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, Product
from cart.models import Cart

# Crear usuarios
User = get_user_model()
user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password123')

# Crear categorías
category1 = Category.objects.create(name='Categoria 1')
category2 = Category.objects.create(name='Categoria 2')

# Crear productos
for i in range(1, 11):
    product = Product.objects.create(
        name=f'Producto {i}',
        price=10.00 + i,
        description=f'Descripción del producto {i}',
        image_url=f'https://dummyimage.com/600x400/828282/000000.jpg&text=Producto+{i}',
        available=True,
        available_units=10
    )
    # Asignar categorías
    if i % 2 == 0:
        product.categories.set([category1])
    else:
        product.categories.set([category2])

# Crear carritos
cart1 = Cart.objects.create(user=user1, paid=False)
cart2 = Cart.objects.create(user=user2, paid=False)

# Agregar productos a los carritos
cart1.products.add(Product.objects.get(name='Producto 1'))
cart1.products.add(Product.objects.get(name='Producto 2'))
cart2.products.add(Product.objects.get(name='Producto 3'))
cart2.products.add(Product.objects.get(name='Producto 4'))

print("Datos insertados correctamente.")
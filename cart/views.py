from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartProduct
from products.models import Product
from django.http import JsonResponse
from urllib.parse import quote

def cart_detail(request):
    # Recuperar el carrito desde la sesión
    cart = request.session.get('cart', {})
    cart_products = []
    total_price = 0
    
    # Para cada producto en el carrito, recuperar sus datos y armar la lista
    for prod_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=prod_id_str)
        item_total = product.price * quantity
        total_price += item_total
        cart_products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(request, 'cart/detail.html', {
        'cart_products': cart_products,
        'total_price': total_price
    })

def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    prod_id_str = str(product_id)
    quantity = int(request.POST.get('quantity', 1))

    if prod_id_str in cart:
        # Ajustar la cantidad
        product = get_object_or_404(Product, id=product_id)
        if quantity > product.available_units:
            quantity = product.available_units
        cart[prod_id_str] = max(quantity, 1)  # mínimo 1

    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.GET.get('quantity', 1))

    cart = request.session.get('cart', {})

    prod_id_str = str(product_id)
    if prod_id_str in cart:
        new_quantity = cart[prod_id_str] + quantity
        cart[prod_id_str] = new_quantity if new_quantity <= product.available_units else product.available_units
    else:
        cart[prod_id_str] = quantity if quantity <= product.available_units else product.available_units

    product.number_of_units_added_to_carts += 1
    product.save()

    request.session['cart'] = cart

    cart_count = len(cart)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'cart_count': cart_count})

    return redirect('products_all')


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    prod_id_str = str(product_id)
    
    if prod_id_str in cart:
        del cart[prod_id_str]
    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_count = len(cart)
        return JsonResponse({'cart_count': cart_count})

    return redirect('cart_detail')





def build_whatsapp_message(request):
    cart = request.session.get('cart', {})
    cart_products = []
    total_price = 0
    store_name = "Mi Tienda"  # Nombre de tu negocio

    # Procesar items del carrito
    for prod_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=prod_id_str)
        item_total = product.price * quantity
        total_price += item_total
        cart_products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    # Construir mensaje desde el cliente
    message_body = (
        f"¡Hola {store_name}! 👋\n"
        "Quiero realizar el siguiente pedido:\n\n"
        "📋 *Detalles del pedido:*\n"
    )

    # Lista de productos
    for i, item in enumerate(cart_products, 1):
        message_body += (
            f"\n{i}. *{item['product'].name}*\n"
            f"   ▸ Cantidad: {item['quantity']} "
            f"{'unidad' if item['quantity'] == 1 else 'unidades'}\n"
            f"   ▸ Precio unitario: C${item['product'].price:,.2f}\n"
            f"   ▸ Subtotal: C${item['item_total']:,.2f}\n"
        )

    # Datos del cliente y total
    message_body += (
        "\n--------------------------------\n"
        f"💵 *Total del pedido: C${total_price:,.2f}*\n\n"
        "📌 *Mis datos de contacto:*\n"
        "   ▸ Nombre: [Tu nombre completo]\n"
        "   ▸ Dirección de envío: [Dirección detallada]\n"
        "   ▸ Teléfono: [Número de contacto]\n"
        "   ▸ Método de pago preferido: [Efectivo/Tarjeta/Transferencia]\n\n"
        "Por favor confirmen disponibilidad y envíen detalles para finalizar la compra. "
        "¡Gracias! 😊\n"
        f"#PedidoOnline{store_name.replace(' ', '')}"
    )

    # Codificar y generar enlace de WhatsApp
    encoded_message = quote(message_body)
    whatsapp_url = f"https://api.whatsapp.com/send?phone=+50582529355&text={encoded_message}"
    
    return redirect(whatsapp_url)
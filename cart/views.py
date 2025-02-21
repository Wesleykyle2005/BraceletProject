from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartProduct
from products.models import Product
from django.http import JsonResponse
from urllib.parse import urlencode

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
    
    for prod_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=prod_id_str)
        item_total = product.price * quantity
        total_price += item_total
        cart_products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })
    
    message_body = "Tu carrito de compras:\n\n"
    for item in cart_products:
        message_body += f"{item['product'].name} - {item['quantity']} unidades - C${item['item_total']:.2f}\n"
    message_body += f"\nTotal: C${total_price:.2f}"
    
    whatsapp_url = "https://api.whatsapp.com/send?" + urlencode({'phone': '+50582529355', 'text': message_body})
    return redirect(whatsapp_url)
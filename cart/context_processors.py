def cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = len(cart)
    return {'cart_count': cart_count}
from django.shortcuts import render
from products.models import Product

# Create your views here.

def home(request):
    products = Product.objects.filter(
        available=True,
        number_of_units_added_to_carts__gt=0
    ).order_by('-number_of_units_added_to_carts', '-created')[:5]
    return render(
        request,
        'core/home.html',
        {
            'products': products
        }
    )


def about(request):
    return render(request, 'core/about.html')
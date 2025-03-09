from django.shortcuts import render
from .models import Product, Category
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator

def products(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(available=True, categories__id=category_id).order_by('-created')
    else:
        products = Product.objects.filter(available=True).order_by('-created')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    
    return render(
        request,
        'products/products.html',
        {
            'products': page_obj,
            'categories': categories,
        }
    )


def filter_products(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(available=True, categories__id=category_id).order_by('-created')
    else:
        products = Product.objects.filter(available=True).order_by('-created')
    
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = []
    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'category': product.categories.all()[0].name if product.categories.exists() else '',
            'description': product.description,
            'price': product.price,
            'image_url': product.image_url,
            'available_units': product.available_units
        })
    
    categories = Category.objects.all()
    
    return render(
        request,
        'products/products.html',
        {
            'products': page_obj,
            'categories': categories,
        }
    )
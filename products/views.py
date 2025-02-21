from django.shortcuts import render
from .models import Product, Category
from django.template.loader import render_to_string
from django.http import JsonResponse

def products(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(available=True, categories__id=category_id).order_by('-created')
    else:
        products = Product.objects.filter(available=True).order_by('-created')
    
    categories = Category.objects.all()
    
    return render(
        request,
        'products/products.html',
        {
            'products': products,
            'categories': categories,
        }
    )


def filter_products(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(available=True, categories__id=category_id).order_by('-created')
    else:
        products = Product.objects.filter(available=True).order_by('-created')
    
    html = render_to_string('products/product_list.html', {'products': products})
    return JsonResponse({'html': html})
from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.products, name='products_all'),
     path('filter/', views.filter_products, name='filter_products'),
]
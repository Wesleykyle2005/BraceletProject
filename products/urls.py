from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('filter/', views.filter_products, name='filter_products'),  
]
from django.urls import path
from . import views
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
     path('send_whatsapp/', views.build_whatsapp_message, name='build_whatsapp_message'),
    
    
]

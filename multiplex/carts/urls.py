from django.urls import path
from . import views


app_name = "carts"

urlpatterns = [
    path('product_cart_add/', views.product_cart_add, name='product_cart_add'),
    path('product_cart_change/', views.product_cart_change, name='product_cart_change'),
    path('product_cart_remove/', views.product_cart_remove, name='product_cart_remove'),
]

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('<int:session_id>/', views.cart_detail, name='cart_detail'),
    path('add/<int:session_id>/<int:row>/<int:place>/', views.cart_add, name='cart_add'),
    path('remove/<int:ticket_id>/', views.cart_remove, name='cart_remove'),
    path('product_cart/', views.product_cart_detail, name='product_cart_detail'),
    path('product_add/<int:product_id>/', views.product_cart_add, name='product_cart_add'),
    path('product_remove/<int:product_id>/', views.product_cart_remove, name='product_cart_remove'),
]
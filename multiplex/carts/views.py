from django.http import JsonResponse
from django.shortcuts import render, redirect

from cinema.models import Product
from carts.models import ProductCart
from django.template.loader import render_to_string

from carts.utils import get_user_carts


def product_cart_add(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = ProductCart.objects.filter(user=request.user, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            ProductCart.objects.create(user=request.user, product=product, quantity=1)
    else:
        carts = ProductCart.objects.filter(
            session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            ProductCart.objects.create(
                session_key=request.session.session_key, product=product, quantity=1)
            
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"product_carts": user_cart}, request=request)

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)


def product_cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = ProductCart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()

    carts = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"product_carts": carts}, request=request)

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)


def product_cart_remove(request):
    cart_id = request.POST.get('cart_id')
    cart = ProductCart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()
    
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"product_carts": user_cart}, request=request)

    response_data = {
        "cart_items_html": cart_items_html,
        'quantity_deleted': quantity,
    }

    return JsonResponse(response_data)

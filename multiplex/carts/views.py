from django.template.loader import render_to_string
from django.http import JsonResponse
from cinema.models import Product, Ticket, Session
from cinema.utils import get_places
from carts.models import ProductCart, TicketCart
from carts.utils import get_user_carts, get_user_ticket_carts




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
    product_carts = get_user_carts(request)
    product_cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"product_carts": product_carts}, request=request)

    ticket_carts = get_user_ticket_carts(request)
    ticket_cart_items_html = render_to_string(
        "carts/includes/ticket_included_cart.html", {"ticket_carts": ticket_carts}, request=request)
    
    response_data = {
        "message": "Товар добавлен в корзину",
        "product_cart_items_html": product_cart_items_html,
        "ticket_cart_items_html": ticket_cart_items_html,
        "price": int(product.sell_price())
    }

    return JsonResponse(response_data)


def product_cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = ProductCart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()

    product_carts = get_user_carts(request)
    product_cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"product_carts": product_carts}, request=request)

    ticket_carts = get_user_ticket_carts(request)
    ticket_cart_items_html = render_to_string(
        "carts/includes/ticket_included_cart.html", {"ticket_carts": ticket_carts}, request=request)
    
    response_data = {
        "message": "Товар добавлен в корзину",
        "product_cart_items_html": product_cart_items_html,
        "ticket_cart_items_html": ticket_cart_items_html,
        "price": int(cart.product.sell_price())
    }

    return JsonResponse(response_data)


def product_cart_remove(request):
    cart_id = request.POST.get('cart_id')
    cart = ProductCart.objects.get(id=cart_id)
    price = cart.product.sell_price() * cart.quantity
    cart.delete()
    
    product_carts = get_user_carts(request)
    product_cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"product_carts": product_carts}, request=request)

    ticket_carts = get_user_ticket_carts(request)
    ticket_cart_items_html = render_to_string(
        "carts/includes/ticket_included_cart.html", {"ticket_carts": ticket_carts}, request=request)
    
    response_data = {
        "message": "Товар добавлен в корзину",
        "product_cart_items_html": product_cart_items_html,
        "ticket_cart_items_html": ticket_cart_items_html,
        "price": int(price)
    }

    return JsonResponse(response_data)



def ticket_cart_add(request):
    session_id = request.POST.get('session_id')
    row = request.POST.get('row')
    place = request.POST.get('place')
    session = Session.objects.get(id=session_id)
    ticket = Ticket.objects.create(session=session, row=row, place=place)

    if request.user.is_authenticated:
        TicketCart.objects.create(user=request.user, ticket=ticket)
    else:
        TicketCart.objects.create(session_key=request.session.session_key, ticket=ticket)
        
    # Перерисовка корзин с билетами        
    ticket_carts = get_user_ticket_carts(request)
    ticket_cart_items_html = render_to_string(
        "carts/includes/ticket_included_cart.html", {"ticket_carts": ticket_carts}, request=request)
    
    # Перерисовка корзины с товарами 
    product_carts = get_user_carts(request)
    product_cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"product_carts": product_carts}, request=request)

    # Перерисовка зала 
    row_info = get_places(session_id) 
    places_html = render_to_string(
        "cinema/includes/places.html", {'row_info': row_info, "session_id": session_id}, request=request
    )
    
    response_data = {
        "message": "Билет добавлен в корзину",
        "ticket_cart_items_html": ticket_cart_items_html,
        "product_cart_items_html": product_cart_items_html,
        "places_html": places_html,
        "price": session.price
    }
    return JsonResponse(response_data)


def ticket_cart_remove(request):
    cart_id = request.POST.get('cart_id')
    cart = TicketCart.objects.get(id=cart_id)
    session_id = cart.ticket.session.id
    price = cart.ticket.session.price
    cart.ticket.delete()
    cart.delete()

    ticket_carts = get_user_ticket_carts(request)
    ticket_cart_items_html = render_to_string(
        "carts/includes/ticket_included_cart.html", {"ticket_carts": ticket_carts}, request=request)
    
    row_info = get_places(session_id) 
    places_html = render_to_string(
        "cinema/includes/places.html", {'row_info': row_info, "session_id": session_id}, request=request
    )
    
    product_carts = get_user_carts(request)
    product_cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"product_carts": product_carts}, request=request)
    
    response_data = {
        "message": "Билет добавлен в корзину",
        "ticket_cart_items_html": ticket_cart_items_html,
        "product_cart_items_html": product_cart_items_html,
        "places_html": places_html,
        "price": price
    }

    return JsonResponse(response_data)
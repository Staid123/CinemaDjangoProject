from django.shortcuts import render, redirect, get_object_or_404
from cinema.models import Movie, Session, Ticket, Product

from .cart import Cart, ProductCart
from .forms import CartAddProductForm


def cart_add(request, session_id, row, place):
    cart = Cart(request)
    session = get_object_or_404(Session, id=session_id)
    ticket = Ticket.objects.create(session=session, row=row, place=place)
    cart.add(ticket=ticket)
    return redirect('cart:cart_detail', session.id)


def cart_remove(request, ticket_id):
    cart = Cart(request)
    ticket = get_object_or_404(Ticket, id=ticket_id)
    session_id = ticket.session.id
    cart.remove(ticket)
    ticket.delete()

    # Если корзина пуста, очищаем ее
    if not cart:
        cart.clear()
    return redirect('cart:cart_detail', session_id)


def cart_detail(request, session_id):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart, 'session_id': session_id})


def product_cart_detail(request):
    product_cart = ProductCart(request)
    for item in product_cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'cart/product_detail.html', {'product_cart': product_cart})


def product_cart_add(request, product_id):
    product_cart = ProductCart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        product_cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:product_cart_detail')


def product_cart_remove(request, product_id):
    product_cart = ProductCart(request)
    product = get_object_or_404(Product, id=product_id)
    product_cart.remove(product)
    if not product_cart:
        product_cart.clear()
        return redirect('cinema:products')
    return redirect('cart:product_cart_detail')
from django.shortcuts import render, redirect, get_object_or_404
from cinema.models import Movie, Session, Ticket, Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_add(request, session_id, row, place, product_id):
    cart = Cart(request)
    session = get_object_or_404(Session, id=session_id)
    ticket = Ticket.objects.create(session=session, row=row, place=place)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(ticket=ticket, product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')


def cart_remove(request, ticket_id):
    cart = Cart(request)
    ticket = get_object_or_404(Ticket, id=ticket_id)
    cart.remove(ticket)
    ticket.delete()
    if not cart:
        return redirect('cinema:select_place', ticket.session.id)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

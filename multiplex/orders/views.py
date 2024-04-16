from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render

from carts.utils import get_user_carts, get_user_ticket_carts
from orders.forms import CreateOrderForm
from orders.models import Order, OrderProductItem, OrderTicketItem


@login_required
def create_order(request):
    ticket_carts = get_user_ticket_carts(request)
    product_carts = get_user_carts(request)
    total_price = ticket_carts.total_price() + product_carts.total_price()

    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    product_cart_items = ticket_carts
                    ticket_cart_items = product_carts

                    if product_cart_items.exists() or ticket_cart_items.exists():
                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            email=form.cleaned_data['email']
                        )
                        # Создать заказанные товары
                        for product_cart_item in product_cart_items:
                            product=product_cart_item.product
                            price=product_cart_item.product.sell_price()
                            quantity=product_cart_item.quantity

                            OrderProductItem.objects.create(
                                order=order,
                                product=product,
                                price=price,
                                quantity=quantity,
                            )
                        
                        # Создать заказанные билеты
                        for ticket_cart_item in ticket_cart_items:
                            ticket = ticket_cart_item.ticket
                            price = ticket.session.price

                            OrderTicketItem.objects.create(
                                order=order,
                                ticket=ticket,
                                price=price,
                            )

                        # Очистить корзину пользователя после создания заказов
                        product_cart_items.delete()
                        ticket_cart_items.delete()
                        messages.success(request, 'Заказ оформлен!')
                        return redirect('users:profile')
            except Exception as e:
                messages.success(request, str(e))
                return redirect('carts:create_order')

    else:
        initial = {
            'first_name': request.user.first_name,
            'phone_number': request.user.phone_number,
            'email': request.user.email
            }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'total_price': total_price
    }
    return render(request, 'orders/create_order.html', context=context)
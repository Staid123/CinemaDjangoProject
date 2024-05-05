from celery_singleton import Singleton
from celery import shared_task
import time
from carts.models import ProductCart, TicketCart


@shared_task(base=Singleton)
def clear_carts(user_id=None, session_key=None):
    if user_id:
        product_carts = ProductCart.objects.filter(user__id=user_id)
        ticket_carts = TicketCart.objects.filter(user__id=user_id)
    else:
        product_carts = ProductCart.objects.filter(session_key=session_key)
        ticket_carts = TicketCart.objects.filter(session_key=session_key)
    for ticket_cart in ticket_carts:
        ticket_cart.ticket.delete()
    product_carts.delete()
    ticket_carts.delete()

    


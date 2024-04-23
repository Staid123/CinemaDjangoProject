from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Prefetch

from orders.models import Order
from orders.models import OrderProductItem, OrderTicketItem


@shared_task
def send_message_email(order_id):
    order = Order.objects.filter(id=order_id).prefetch_related(
                Prefetch(
                    "orderproductitem_set",
                    queryset=OrderProductItem.objects.select_related("product"),
                ),
                Prefetch(
                    "orderticketitem_set",
                    queryset=OrderTicketItem.objects.select_related("ticket"),
                )
            ).first()
    orderproductitem_info = ", ".join(str(orderproductitem.product) for orderproductitem in order.orderproductitem_set.all())
    orderticketitem_info = ", ".join(str(orderticketitem.ticket) for orderticketitem in order.orderticketitem_set.all())
    send_mail(
        f"Ваш заказ {order.id}", 
        f"Билеты: {orderticketitem_info}\nТовары: {orderproductitem_info}", 
        "multiplex@gmail.com", 
        [order.user.email])
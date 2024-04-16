from django.db import models
from cinema.models import Product, Ticket

from users.models import User


class OrderItemProductQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(max_length=50, verbose_name="Електронная почта")

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name}"


class OrderProductItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт", default=None)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")


    class Meta:
        db_table = "order_product_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderItemProductQueryset.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f"Товар {self.product.name} | Заказ товара № {self.order.pk}"
    

class OrderItemCartQueryset(models.QuerySet):
    def total_price(self):
        return sum(int(cart.ticket.session.price) for cart in self)
    
    def total_quantity(self):
        if self:
            return len(self)
        return 0
        

class OrderTicketItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    ticket = models.ForeignKey(to=Ticket, on_delete=models.SET_DEFAULT, null=True, verbose_name="Билет", default=None)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")


    class Meta:
        db_table = "order_ticket_item"
        verbose_name = "Проданный билет"
        verbose_name_plural = "Проданные билеты"

    objects = OrderItemCartQueryset.as_manager()

    def __str__(self):
        return f"Билет {self.ticket.id} | Заказ билета № {self.order.pk}"
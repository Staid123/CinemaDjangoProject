from django.db import models

from cinema.models import Product, Ticket
from users.models import User


class ProductCartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class ProductCart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')

    class Meta:
        db_table = 'product_cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ("id",)

    objects = ProductCartQueryset().as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        if self.user:
            return f'Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}'
        return f'Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}'


class TicketCartQuerySet(models.QuerySet):
    def total_price(self):
        return sum(cart.ticket.session.price for cart in self)
    
    def total_quantity(self):
        if self:
            return len(self)
        return 0
    
    def movie(self):
        if self:
            return self[0].ticket.session.movie


class TicketCart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, verbose_name="Товар")
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')

    class Meta:
        db_table = 'ticket_cart'
        verbose_name = "Корзина с билетами"
        verbose_name_plural = 'Корзины с билетами'
        ordering = ("id",)
    
    objects = TicketCartQuerySet().as_manager()

    def __str__(self):
        if self.user:
            return f'Корзина с билетами {self.user.username} | Билет {self.ticket.id} | Ряд {self.ticket.row} | Место {self.ticket.place}'
        return f'Анонимная корзина с билетами | Билет {self.ticket.id} | Ряд {self.ticket.row} | Место {self.ticket.place}'
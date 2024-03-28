from decimal import Decimal
from django.conf import settings
from cinema.models import Movie, Session, Ticket


class Cart:
    def __init__(self, request):
        """
        Инициализировать корзину.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, ticket):
        """
         Добавить товар в корзину либо обновить.
         """
        ticket_id = str(ticket.id)
        if ticket_id not in self.cart:
            self.cart[ticket_id] = {
                'row': ticket.row,
                'place': ticket.place,
            }
        self.save()
        print(self.cart)

    def save(self):
        # пометить сеанс как "измененный",
        # чтобы обеспечить его сохранение
        self.session.modified = True

    def remove(self, ticket):
        """
        Удалить товар из корзины.
        """
        ticket_id = str(ticket.id)
        if ticket_id in self.cart:
            del self.cart[ticket_id]
            self.save()

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле и
        получить товары из базы данных.
        """
        ticket_ids = self.cart.keys()
        # получить объекты product и добавить их в корзину
        tickets = Ticket.objects.filter(id__in=ticket_ids)
        cart = self.cart.copy()
        for ticket in tickets:
            cart[str(ticket.id)]['ticket'] = ticket
        for item in cart.values():
            yield item

    def __len__(self):
        return len(self.cart.keys())

    def get_total_price(self):
        return sum(Decimal(item['ticket'].session.price) for item in self.cart.values())

    def clear(self):
        # удалить корзину из сеанса
        del self.session[settings.CART_SESSION_ID]
        self.save()

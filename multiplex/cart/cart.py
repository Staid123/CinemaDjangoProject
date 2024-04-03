from decimal import Decimal
from django.conf import settings
from cinema.models import Movie, Session, Ticket, Product


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
        ticket_id = str(ticket.id)
        if ticket_id not in self.cart:
            self.cart[ticket_id] = {
                'row': ticket.row,
                'place': ticket.place,
            }
        self.save()

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


class ProductCart:
    def __init__(self, request):
        """
        Инициализировать корзину.
        """
        self.session = request.session
        product_cart = self.session.get(settings.PRODUCT_CART_SESSION_ID)
        if not product_cart:
            # сохранить пустую корзину в сеансе
            product_cart = self.session[settings.PRODUCT_CART_SESSION_ID] = {}
        self.product_cart = product_cart

    def add(self, product, quantity=1, override_quantity=False):
        """
         Добавить товар в корзину либо обновить его количество.
         """
        product_id = str(product.id)
        if product_id not in self.product_cart:
            self.product_cart[product_id] = {'quantity': 0,
                                             'price': str(product.price)}
        if override_quantity:
            self.product_cart[product_id]['quantity'] = quantity
        else:
            self.product_cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # пометить сеанс как "измененный",
        # чтобы обеспечить его сохранение
        self.session.modified = True

    def remove(self, product):
        """
        Удалить товар из корзины.
        """
        product_id = str(product.id)
        if product_id in self.product_cart:
            del self.product_cart[product_id]
        self.save()

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле и
        получить товары из базы данных.
        """
        product_ids = self.product_cart.keys()
        # получить объекты product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        product_cart = self.product_cart.copy()
        for product in products:
            product_cart[str(product.id)]['product'] = product
        for item in product_cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчитать все товарные позиции в корзине.
        """
        return sum(item['quantity'] for item in self.product_cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.product_cart.values())

    def clear(self):
        # удалить корзину из сеанса
        del self.session[settings.PRODUCT_CART_SESSION_ID]
        self.save()

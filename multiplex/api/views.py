from rest_framework import viewsets, permissions
from cinema.models import Movie, Genre, Session, Hall, Ticket, Product
from api import serializers
from rest_framework.response import Response
from users.models import User
from carts.models import ProductCart



class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = serializers.MovieSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = serializers.SessionSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = serializers.HallSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'number'


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ProductCartViewSet(viewsets.ModelViewSet):
    queryset = ProductCart.objects.all()
    serializer_class = serializers.ProductCartSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'username'
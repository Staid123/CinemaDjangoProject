from rest_framework import serializers
from cinema.models import Movie, Genre, Session, Hall, Ticket, Product
from carts.models import ProductCart
from users.models import User


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='movie-detail',
        lookup_field='slug'
    )

    genre = serializers.HyperlinkedRelatedField(
        view_name='genre-detail',
        lookup_field='slug',
        many=True,
        read_only=True
    )

    class Meta:
        model = Movie
        fields = "__all__"
    

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'session-detail',
        lookup_field = 'pk'
    )
    movie = serializers.HyperlinkedRelatedField(
        view_name = 'movie-detail',
        lookup_field = 'slug',
        read_only=True
    )
    hall = serializers.HyperlinkedRelatedField(
        view_name = 'hall-detail',
        lookup_field = 'number',
        read_only=True
    )
    class Meta:
        model = Session
        fields = '__all__'


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = "__all__"


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'ticket-detail',
        lookup_field = 'pk'
    )
    session = serializers.HyperlinkedRelatedField(
        view_name = 'session-detail',
        lookup_field = 'pk',
        read_only = True
    )
    class Meta:
        model = Ticket
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCartSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='productcart-detail',
        lookup_field = 'pk'
    )
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        read_only=True
    )
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail',
        lookup_field='slug',
        read_only=True
    )
    session_key = serializers.CharField(read_only=True)
    class Meta:
        model = ProductCart
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

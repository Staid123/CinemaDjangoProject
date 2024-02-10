from django.shortcuts import render
from . import services
from django.shortcuts import get_object_or_404
from .models import Movie


def home_view(request):

    """ Главная страница """

    movies = services.get_all_movies()
    return render(request, 'cinema/index.html', {'movies': movies})


def show_post(request, movie_slug):

    """ Подробнее о фильме """

    movie = get_object_or_404(Movie, slug=movie_slug)
    return render(request, 'cinema/post.html', {'movie': movie})

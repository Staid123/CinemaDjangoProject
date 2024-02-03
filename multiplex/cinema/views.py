from django.shortcuts import render
from . import services


def home_view(request):
    """ Главная страница """
    movies = services.get_all_movies()
    return render(request, 'cinema/index.html', {'movies': movies})

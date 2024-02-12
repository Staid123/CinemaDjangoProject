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

    hours, remainder = divmod(int(movie.duration), 60)
    movie.duration = f"{hours}:{remainder:02d}"

    movies = services.get_random_movies(movie)

    dates = list(set(movie.session.values_list('date', flat=True).order_by('date')))

    sessions_by_date = {}

    for date in dates:
        time_list = list(movie.session.filter(date=date).values_list('time', flat=True))
        sessions_by_date[date] = time_list

    return render(request, 'cinema/post.html', {'movie': movie, 'movies': movies, 'dates': sessions_by_date})

from django.shortcuts import render
from . import services
from django.shortcuts import get_object_or_404
from .models import Movie
from collections import defaultdict

def home_view(request):

    """ Главная страница """

    pusblished_movies = services.get_published_movies()
    return render(request, 'cinema/index.html', {'movies': pusblished_movies})


def show_post(request, movie_slug):

    """ Подробнее о фильме """

    movie = get_object_or_404(Movie, slug=movie_slug)

    hours, remainder = divmod(int(movie.duration), 60)
    movie.duration = f"{hours}:{remainder:02d}"

    movies = services.get_random_movies(movie)

    dates = movie.session.order_by('date').values_list('date', flat=True).distinct()
    sessions_by_date = {}

    for date in dates:
        hall_and_times = {}
        hall_num_list = list(movie.session.filter(date=date).values_list('hall', flat=True))
        for hall in hall_num_list:
            time_list = list(movie.session.filter(date=date, hall=hall).values_list('time', flat=True))
            hall_and_times[hall] = time_list
        sessions_by_date[date] = hall_and_times

    return render(request, 'cinema/post.html', {'movie': movie, 'movies': movies, 'sessions_by_date': sessions_by_date})


def show_movies(request):

    """Распределение фильмов на 'Сейчас в кино', 'Скоро в прокате', 'Архив'"""

    published = services.get_published_movies()
    soon = services.get_soon_movies()
    archived = services.get_archived_movies()
    movies = {'published': published, 'soon': soon, 'archived': archived}

    return render(request, 'cinema/movies.html', {'movies': movies})


from django.shortcuts import render
from . import services
from django.shortcuts import get_object_or_404
from .models import Movie


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


def show_movies(request, status):

    """Распределение фильмов на 'Сейчас в кино', 'Скоро в прокате', 'Архив'"""

    eng_status = {"soon": "Скоро в прокате", "now": "Опубликован", "archive": "Архив"}

    movies = services.get_movies_by_status(eng_status[status])

    return render(request, 'cinema/movies.html', {'movies': movies, 'status': status})


def soon_movies(request):
    """Отображение фильмов категории 'скоро в прокате' по датам"""

    movies = services.get_soon_movies()
    date_and_movies = dict()

    for movie in movies:
        if movie.start_of_rental not in date_and_movies.keys():
            date_and_movies[movie.start_of_rental] = [
                {'movie': movie,
                 'day_of_week': services.get_day_of_week(str(movie.start_of_rental))
                 }]
        else:
            date_and_movies[movie.start_of_rental].append({
                'movie': movie,
                'day_of_week': services.get_day_of_week(str(movie.start_of_rental))
            })

    return render(request, 'cinema/soon.html', {'date_and_movies': date_and_movies})


def show_products(request):
    """Отображение товаров"""

    products = services.get_products()
    return render(request, 'cinema/products.html', {'products': products})

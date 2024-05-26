from django.shortcuts import render
from django.shortcuts import get_object_or_404

from carts.utils import get_user_ticket_carts, get_user_carts
from . import services
from .models import Movie, Session


def home_view(request):

    """ Главная страница """

    pusblished_movies = services.get_published_movies()
    return render(request, 'cinema/index.html', {'movies': pusblished_movies})


def show_post(request, movie_slug):

    """ Подробнее о фильме """

    movie = get_object_or_404(Movie, slug=movie_slug)

    hours, remainder = divmod(int(movie.duration), 60)
    movie.duration = f"{hours}:{remainder:02d}"

    published_movies = services.get_random_published_movies(movie)
    soon1_movies = services.get_random_soon_movies(movie)

    sessions = Session.objects.filter(movie=movie).order_by('date', 'time')
    sessions_by_date = {}

    for session in sessions:
        if session.date not in sessions_by_date.keys():
            sessions_by_date[session.date] = []
        sessions_by_date[session.date].append({session.id: session.time})

    return render(request, 'cinema/post.html', {'movie': movie, 'published_movies': published_movies, 'soon_movies': soon1_movies, 'sessions': sessions_by_date})


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
    ticket_carts = get_user_ticket_carts(request)
    return render(request, 'cinema/products.html', {'products': products, 'ticket_carts': ticket_carts})


def select_place(request, session_id):
    session = Session.objects.get(id=session_id)
    ticket_carts = get_user_ticket_carts(request)
    product_carts = get_user_carts(request)
    total_price = ticket_carts.total_price() + product_carts.total_price()
    return render(request, 'cinema/select_place.html', {
        'session': session,
        'total_price': total_price
    })



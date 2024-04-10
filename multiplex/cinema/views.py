from django.shortcuts import render

from . import services
from django.shortcuts import get_object_or_404
from .models import Movie, Session
# from cart.forms import CartAddProductForm

# from cart.cart import Cart, ProductCart


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

    sessions = Session.objects.filter(movie=movie).order_by('date', 'time')
    sessions_by_date = {}

    for session in sessions:
        if session.date not in sessions_by_date.keys():
            sessions_by_date[session.date] = []
        sessions_by_date[session.date].append({session.id: session.time})

    return render(request, 'cinema/post.html', {'movie': movie, 'movies': movies, 'sessions': sessions_by_date})


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


def select_place(request, session_id):
    session = Session.objects.get(id=session_id)
    rows = [int(num) for num in range(1, int(session.hall.places / 10) + 1)]
    count_places_in_every_row = [num for num in range(1, 10)]
    row_info = {}
    for row_num in rows:
        reserved_seats = session.tickets.filter(session=session, row=row_num).values_list('place', flat=True)
        row_info[row_num] = [{
            'count_places': count_places_in_every_row,
            'reserved_seats': list(reserved_seats)
        }]
    # {row_num: [{'count_places': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'reserved_seats': [place_num, place_num]}]
    return render(request, 'cinema/select_place.html', {
        'session': session,
        'row_info': row_info
    })



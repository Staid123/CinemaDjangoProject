from django.db.models import QuerySet
from datetime import date, datetime
from . import models
import calendar


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya', 'й': 'i'}

    return "".join(map(lambda x: d[x] if x in d.keys() else x, s.lower()))


def get_published_movies() -> QuerySet:
    """
    Получение опубликованных записей
    :return: QuerySet
    """
    return models.Movie.objects.filter(status=models.Movie.STATUS_CHOICES[1][0])


def get_movies_by_status(status) -> QuerySet:
    """
    Получение ожидаемых записей
    :return: QuerySet
    """
    return models.Movie.objects.filter(status=status)


def get_soon_movies() -> QuerySet:
    """
    Получение ожидаемых записей
    :return: QuerySet
    """
    return models.Movie.objects.filter(status=models.Movie.STATUS_CHOICES[0][0]).order_by('start_of_rental')


def get_random_published_movies(exclude_movie) -> QuerySet:
    """
    Получаем 5 случайных фильма, исключая переданный movie,
    с сортировкой по времени создания в обратном порядке
    """
    random_movies = models.Movie.objects.filter(status="Опубликован").exclude(id=exclude_movie.id).order_by('start_of_rental')[:5]
    return random_movies


def get_random_soon_movies(exclude_movie) -> QuerySet:
    """
    Получаем 5 случайных фильма, исключая переданный movie,
    с сортировкой по времени создания в обратном порядке
    """
    random_movies = models.Movie.objects.filter(status="Скоро в прокате").exclude(id=exclude_movie.id).order_by('start_of_rental')[:5]
    return random_movies


def get_day_of_week(date_str):
    """
    Перевод даты в день недели
    """
    ru_day_name = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье"
    }
    date_object = datetime.strptime(date_str, '%Y-%m-%d')
    day_of_week = date_object.weekday()
    day_name = calendar.day_name[day_of_week]
    return ru_day_name[day_name]


def get_products():
    """Получение всех продуктов"""
    return models.Product.objects.all()
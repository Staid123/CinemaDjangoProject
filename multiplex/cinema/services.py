from django.db.models import QuerySet
from datetime import date
from . import models


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


def get_archived_movies() -> QuerySet:
    """
    Получение записей с архива
    :return: QuerySet
    """
    return models.Movie.objects.filter(status=models.Movie.STATUS_CHOICES[2][0])


def get_soon_movies() -> QuerySet:
    """
    Получение ожидаемых записей
    :return: QuerySet
    """
    return models.Movie.objects.filter(status=models.Movie.STATUS_CHOICES[0][0])


def get_random_movies(exclude_movie) -> QuerySet:
    """
    Получаем три случайных фильма, исключая переданный movie,
    с сортировкой по времени создания в обратном порядке
    """
    random_movies = models.Movie.objects.exclude(id=exclude_movie.id).order_by('start_of_rental')[:5]
    return random_movies

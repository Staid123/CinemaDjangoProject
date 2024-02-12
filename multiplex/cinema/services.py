from django.db.models import QuerySet

from . import models


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya', 'й': 'i'}

    return "".join(map(lambda x: d[x] if x in d.keys() else x, s.lower()))


def get_all_movies() -> QuerySet:
    """
    Получение всех записей
    :return: QuerySet
    """
    return models.Movie.objects.all()


def get_random_movies(exclude_movie):
    """
    Получаем три случайных фильма, исключая переданный movie,
    с сортировкой по времени создания в обратном порядке
    """
    random_movies = models.Movie.objects.exclude(id=exclude_movie.id).order_by('?').order_by('start_of_rental')[:5]
    return random_movies

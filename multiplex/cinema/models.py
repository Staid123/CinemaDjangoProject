from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from . import services
from django.utils.text import slugify
from django.urls import reverse
from datetime import date


class Movie(models.Model):
    STATUS_CHOICES = [
        ("Скоро в прокате", "Скоро в прокате"),
        ("Опубликован", "Опубликован"),
        ("Архив", "Архив"),
    ]

    title = models.CharField(max_length=50, verbose_name="Название фильма")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)
    preview = models.ImageField(upload_to="preview", verbose_name="Фото")
    years = models.CharField(max_length=3, verbose_name="Возраст")
    description = models.TextField(max_length=1000, verbose_name="Краткое описание")
    genre = models.ManyToManyField("Genre", verbose_name="Жанр", related_name="genres")
    language = models.CharField(max_length=30, verbose_name="Язык")
    start_of_rental = models.DateField(verbose_name="Начало проката")
    end_of_rental = models.DateField(verbose_name="Конец проката")
    release_year = models.CharField(max_length=4, verbose_name="Год релиза")
    producer = models.CharField(max_length=200, verbose_name="Режиссер")
    duration = models.IntegerField(verbose_name="Продолжительность", validators=[
        MinValueValidator(30),
        MaxValueValidator(180)
    ])
    status = models.CharField(
        verbose_name="Статус фильма",
        choices=STATUS_CHOICES,
        default="Скоро в прокате",
        max_length=20,
    )
    starring = models.TextField(max_length=500, verbose_name="В главных ролях")
    production = models.CharField(max_length=20, verbose_name="Производство")
    session = models.ManyToManyField("Session", verbose_name="Информация о фильме", related_name="session")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = services.translit_to_eng(slugify(self.title, allow_unicode=True))

        if date.today() < self.start_of_rental:
            self.status = self.STATUS_CHOICES[0][0]
        elif self.start_of_rental <= date.today() <= self.end_of_rental:
            self.status = self.STATUS_CHOICES[1][0]
        else:
            self.status = self.STATUS_CHOICES[2][0]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('movie', kwargs={'movie_slug': self.slug})

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class Genre(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = services.translit_to_eng(slugify(self.name, allow_unicode=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Session(models.Model):
    date = models.DateField(verbose_name="Дата сеанса")
    time = models.TimeField(verbose_name="Время сеанса")
    hall = models.ForeignKey('Hall', verbose_name="Номер зала", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"

    def __str__(self):
        hall_number = self.hall.number if self.hall else "N/A"
        return f'{self.date} {self.time}, Зал {hall_number}'


class Hall(models.Model):
    number = models.IntegerField(verbose_name="Номер зала")
    places = models.IntegerField(verbose_name="Количество обычных мест")
    vip_places = models.IntegerField(verbose_name="Количество премиум мест")
    price_default_places = models.IntegerField(verbose_name="Стоимость обычных мест")
    price_vip_places = models.IntegerField(verbose_name="Стоимость премиум мест")

    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"

    def __str__(self):
        return f'Зал №{self.number}'


class Product(models.Model):
    name = models.CharField(verbose_name="Название продукта", max_length=255)
    price = models.IntegerField(verbose_name="Цена продукта")
    photo = models.ImageField(upload_to="product_photo", verbose_name="Фото")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f'Продукт {self.name}'

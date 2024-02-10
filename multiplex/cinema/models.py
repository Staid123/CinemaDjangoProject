from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from . import services
from django.utils.text import slugify
from django.urls import reverse


class Movie(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название фильма")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)
    preview = models.ImageField(upload_to="preview")
    years = models.CharField(max_length=3, verbose_name="Возраст")
    description = models.TextField(max_length=1000, verbose_name="Краткое описание")
    genre = models.ManyToManyField("Genre", verbose_name="Жанр", blank=True, related_name="genres")
    language = models.CharField(max_length=30, verbose_name="Язык")
    start_of_rental = models.DateField(verbose_name="Начало проката")
    end_of_rental = models.DateField(verbose_name="Конец проката")
    release_year = models.CharField(max_length=4, verbose_name="Год релиза")
    producer = models.CharField(max_length=200, verbose_name="Режиссер")
    duration = models.IntegerField(verbose_name="Продолжительность", validators=[
        MinValueValidator(30),
        MaxValueValidator(180)
    ])
    starring = models.TextField(max_length=500,verbose_name="В главных ролях")
    production = models.CharField(max_length=20, verbose_name="Производство")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = services.translit_to_eng(slugify(self.title, allow_unicode=True))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

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
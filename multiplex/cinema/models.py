from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from datetime import date, datetime, timedelta
from cinema.tasks import delete_session, rewrite_movie_status


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

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if date.today() < self.start_of_rental:
            self.status = self.STATUS_CHOICES[0][0]
            run_at = self.start_of_rental
            new_status = self.STATUS_CHOICES[1][0]
        elif self.start_of_rental <= date.today() <= self.end_of_rental:
            self.status = self.STATUS_CHOICES[1][0]
            run_at = self.end_of_rental + timedelta(hours=23)
            new_status = self.STATUS_CHOICES[2][0]
        else:
            self.status = self.STATUS_CHOICES[2][0]
        if not self.id:
            super().save(*args, **kwargs)
            rewrite_movie_status.apply_async(args=(self.id, new_status), eta=run_at)
        else:
            super().save(*args, **kwargs)
        

    def get_absolute_url(self):
        return reverse('cinema:movie', kwargs={'movie_slug': self.slug})

    class Meta:
        db_table = 'Films'
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Genres'
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Session(models.Model):
    movie = models.ForeignKey('Movie', verbose_name="Название фильма", on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField(verbose_name="Дата сеанса")
    time = models.TimeField(verbose_name="Время сеанса")
    hall = models.ForeignKey('Hall', verbose_name="Номер зала", on_delete=models.CASCADE, blank=True, null=True, related_name='halls')
    price = models.IntegerField(verbose_name="Стоимость обычных мест")

    class Meta:
        db_table = 'sessions'
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"

    def __str__(self):
        hall_number = self.hall.number if self.hall else "N/A"
        return f'{self.pk} {self.date} {self.time}, Зал {hall_number} Фильм {self.movie.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        run_at = datetime.combine(self.date, self.time)
        delete_session.apply_async(args=(self.id, ), eta=run_at)


class Hall(models.Model):
    number = models.IntegerField(verbose_name="Номер зала")
    places = models.IntegerField(verbose_name="Количество обычных мест")

    class Meta:
        db_table = 'halls'
        verbose_name = "Зал"
        verbose_name_plural = "Залы"

    def __str__(self):
        return f'Зал №{self.number}'


class Ticket(models.Model):
    session = models.ForeignKey('Session', verbose_name="Сессия", on_delete=models.CASCADE, blank=True, null=True, related_name='tickets')
    row = models.IntegerField(verbose_name="Ряд")
    place = models.IntegerField(verbose_name="Место")

    class Meta:
        db_table = 'tickets'
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'

    def __str__(self):
        return f'Фильм {self.session.movie.title} | Зал {self.session.hall.number} | Ряд {self.row} | Место {self.place}'


class Product(models.Model):
    name = models.CharField(verbose_name="Название продукта", max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    photo = models.ImageField(upload_to="product_photo", verbose_name="Фото")
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')

    class Meta:
        db_table = 'product'
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("id",)

    def __str__(self):
        return f'{self.name}'

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price

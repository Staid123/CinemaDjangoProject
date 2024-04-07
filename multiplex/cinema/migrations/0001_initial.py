# Generated by Django 4.2.1 on 2024-04-06 16:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'db_table': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер зала')),
                ('places', models.IntegerField(verbose_name='Количество обычных мест')),
            ],
            options={
                'verbose_name': 'Зал',
                'verbose_name_plural': 'Залы',
                'db_table': 'halls',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название фильма')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('preview', models.ImageField(upload_to='preview', verbose_name='Фото')),
                ('years', models.CharField(max_length=3, verbose_name='Возраст')),
                ('description', models.TextField(max_length=1000, verbose_name='Краткое описание')),
                ('language', models.CharField(max_length=30, verbose_name='Язык')),
                ('start_of_rental', models.DateField(verbose_name='Начало проката')),
                ('end_of_rental', models.DateField(verbose_name='Конец проката')),
                ('release_year', models.CharField(max_length=4, verbose_name='Год релиза')),
                ('producer', models.CharField(max_length=200, verbose_name='Режиссер')),
                ('duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(180)], verbose_name='Продолжительность')),
                ('status', models.CharField(choices=[('Скоро в прокате', 'Скоро в прокате'), ('Опубликован', 'Опубликован'), ('Архив', 'Архив')], default='Скоро в прокате', max_length=20, verbose_name='Статус фильма')),
                ('starring', models.TextField(max_length=500, verbose_name='В главных ролях')),
                ('production', models.CharField(max_length=20, verbose_name='Производство')),
                ('genre', models.ManyToManyField(related_name='genres', to='cinema.genre', verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
                'db_table': 'Films',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Цена')),
                ('photo', models.ImageField(upload_to='product_photo', verbose_name='Фото')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, verbose_name='Скидка в %')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'db_table': 'product',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата сеанса')),
                ('time', models.TimeField(verbose_name='Время сеанса')),
                ('price', models.IntegerField(verbose_name='Стоимость обычных мест')),
                ('hall', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='halls', to='cinema.hall', verbose_name='Номер зала')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='cinema.movie', verbose_name='Название фильма')),
            ],
            options={
                'verbose_name': 'Сеанс',
                'verbose_name_plural': 'Сеансы',
                'db_table': 'sessions',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField(verbose_name='Ряд')),
                ('place', models.IntegerField(verbose_name='Место')),
                ('session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='cinema.session', verbose_name='Сессия')),
            ],
            options={
                'verbose_name': 'Билет',
                'verbose_name_plural': 'Билеты',
                'db_table': 'tickets',
            },
        ),
    ]

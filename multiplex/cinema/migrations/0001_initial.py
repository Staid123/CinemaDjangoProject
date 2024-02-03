# Generated by Django 4.2.1 on 2024-02-03 11:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название фильма')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('preview', models.ImageField(upload_to='preview')),
                ('years', models.CharField(max_length=3, verbose_name='Возраст')),
                ('description', models.CharField(max_length=200, verbose_name='Краткое описание')),
                ('language', models.CharField(max_length=30, verbose_name='Язык')),
                ('start_of_rental', models.DateField(verbose_name='Начало проката')),
                ('end_of_rental', models.DateField(verbose_name='Конец проката')),
                ('release_year', models.CharField(max_length=4, verbose_name='Год релиза')),
                ('producer', models.CharField(max_length=50, verbose_name='Режиссер')),
                ('duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(180)], verbose_name='Продолжительность')),
                ('starring', models.CharField(max_length=255, verbose_name='В главных ролях')),
                ('production', models.CharField(max_length=20, verbose_name='Производство')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
            },
        ),
    ]

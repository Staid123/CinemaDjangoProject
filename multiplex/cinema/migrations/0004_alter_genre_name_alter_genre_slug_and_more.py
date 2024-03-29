# Generated by Django 4.2.1 on 2024-02-03 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0003_alter_genre_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='producer',
            field=models.CharField(max_length=200, verbose_name='Режиссер'),
        ),
    ]

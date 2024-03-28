# Generated by Django 4.2.1 on 2024-03-26 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0003_remove_movie_session_session_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='cinema.movie', verbose_name='Название фильма'),
        ),
    ]

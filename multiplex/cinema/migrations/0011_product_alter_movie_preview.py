# Generated by Django 4.2.1 on 2024-02-21 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0010_movie_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('price', models.IntegerField(verbose_name='Цена продукта')),
                ('photo', models.ImageField(upload_to='product_photo', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.AlterField(
            model_name='movie',
            name='preview',
            field=models.ImageField(upload_to='preview', verbose_name='Фото'),
        ),
    ]

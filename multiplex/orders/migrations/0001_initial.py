# Generated by Django 4.1.13 on 2024-04-14 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cinema', '0003_alter_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=20, verbose_name='Електронная почта')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderTicketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Заказ')),
                ('ticket', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='cinema.ticket', verbose_name='Билет')),
            ],
            options={
                'verbose_name': 'Проданный товар',
                'verbose_name_plural': 'Проданные товары',
                'db_table': 'order_ticket_item',
            },
        ),
        migrations.CreateModel(
            name='OrderProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='cinema.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Проданный товар',
                'verbose_name_plural': 'Проданные товары',
                'db_table': 'order_product_item',
            },
        ),
    ]
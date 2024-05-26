# Generated by Django 4.1.13 on 2024-04-11 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0003_alter_product_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0003_alter_productcart_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=32, null=True)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.ticket', verbose_name='Товар')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина с билетами',
                'verbose_name_plural': 'Корзины с билетами',
                'db_table': 'ticket_cart',
                'ordering': ('id',),
            },
        ),
    ]
# Generated by Django 4.2.1 on 2024-03-26 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0005_alter_session_movie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='num',
            new_name='place',
        ),
    ]

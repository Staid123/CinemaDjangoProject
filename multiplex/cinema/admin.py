from django.contrib import admin
from .models import Movie, Genre, Session

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Session)

admin.site.site_header = "Панель администрирования"

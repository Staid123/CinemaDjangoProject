from django.contrib import admin
from .models import Movie, Genre, Session, Hall

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Session)
admin.site.register(Hall)

admin.site.site_header = "Панель администрирования"

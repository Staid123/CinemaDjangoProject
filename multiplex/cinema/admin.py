from django.contrib import admin
from .models import Movie, Genre, Session, Hall, Product, Ticket


# admin.site.register(Movie)
# admin.site.register(Genre)
# admin.site.register(Session)
# admin.site.register(Hall)
# admin.site.register(Product)
# admin.site.register(Ticket)

admin.site.site_header = "Панель администрирования"


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name', )}
    list_display = ['id', 'name']
    list_editable = ['name']
    search_fields = ['name']
    list_filter: list[str] = ['name']
    fields = ['name']


@admin.register(Movie)
class MoviesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title', )}
    list_display = ['title', 'start_of_rental', 'end_of_rental', 'status']
    list_editable = ['start_of_rental', 'end_of_rental', 'status']
    search_fields = ['title', 'status']
    list_filter: list[str] = ['title']
    fields = [
            'title', 'slug', 'genre', 'start_of_rental', 'end_of_rental', 'preview', 'status',
            'years', 'description',  'language', 'release_year', 
            'producer', 'duration', 'starring', 'production'
    ]


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount']
    list_editable = ['price', 'discount']
    search_fields = ['name']
    list_filter = ['name', 'price', 'discount']
    fields = [
        'name',
        ('price', 'discount')
    ]


@admin.register(Hall)
class HallsAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'places']
    list_editable = ['number', 'places']
    search_fields = ['number']
    list_filter = ['number']



@admin.register(Session)
class SessionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'date', 'time', 'hall', 'price']
    list_editable = ['movie', 'date', 'time', 'hall', 'price']
    list_filter: list[str] = ['movie__title', 'date', 'hall']
    

@admin.register(Ticket)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'row', 'place']
    list_editable = ['session', 'row', 'place']
    list_filter = ['session__movie__title', 'session__hall__number']

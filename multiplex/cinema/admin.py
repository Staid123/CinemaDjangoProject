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
    list_display = ['id', 'name', 'slug']
    list_editable = ['name', 'slug']
    search_fields = ['name', 'slug']
    list_filter: list[str] = ['name', 'slug']
    fields = ['name', 'slug']


@admin.register(Movie)
class MoviesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title', )}
    list_display = ['title', 'start_of_rental', 'end_of_rental', 'status']
    list_editable = ['start_of_rental', 'end_of_rental', 'status']
    search_fields = ['title', 'status']
    list_filter: list[str] = ['title', 'status']
    fields = [
            'title', 'slug', 'genre', 'start_of_rental', 'end_of_rental', 'preview', 'status',
            'years', 'description',  'language', 'release_year', 
            'producer', 'duration', 'starring', 'production'
    ]


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name', )}
    list_display = ['name', 'price', 'discount', 'slug']
    list_editable = ['price', 'discount', 'slug']
    search_fields = ['name', 'slug']
    list_filter = ['name', 'price', 'discount', 'slug']
    fields = [
        'name',
        ('price', 'discount'),
        'photo',
        'slug'
    ]


@admin.register(Hall)
class HallsAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'places']
    list_editable = ['number', 'places']
    search_fields = ['number']
    list_filter = ['number']



@admin.register(Session)
class SessionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'published_movie', 'date', 'time', 'hall', 'price']
    list_editable = ['date', 'time', 'hall', 'price']
    list_filter = ['movie__title', 'date', 'hall']

    @admin.display(description="Фильм (Опубликован)")
    def published_movie(self, obj):
        return obj.movie.title if obj.movie.status == 'Опубликован' else None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(movie__status='Опубликован')

@admin.register(Ticket)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'row', 'place']
    list_editable = ['session', 'row', 'place']
    list_filter = ['session__movie__title', 'session__hall__number']

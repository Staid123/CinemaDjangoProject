from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('movie/<slug:movie_slug>/', views.show_post, name='movie'),
    path('movies/<str:status>/', views.show_movies, name='movies'),
    path('soon/', views.soon_movies, name='soon_movies'),
]

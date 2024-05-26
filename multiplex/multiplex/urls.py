"""
URL configuration for multiplex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from rest_framework import routers
from api import views



router = routers.DefaultRouter()
router.register(r'movie', views.MovieViewSet, basename='movie')
router.register(r'genre', views.GenreViewSet, basename='genre')
router.register(r'session', views.SessionViewSet, basename='session')
router.register(r'hall', views.HallViewSet, basename='hall')
router.register(r'ticket', views.TicketViewSet, basename='ticket')
router.register(r'product', views.ProductViewSet, basename='product')
router.register(r'productcart', views.ProductCartViewSet, basename='productcart')
router.register(r'user', views.UserViewSet, basename='user')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('cinema.urls', namespace="cinema")),
    path('users/', include('users.urls', namespace="users")),
    path('cart/', include('carts.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('api-auth/', include('rest_framework.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
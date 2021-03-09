from character_finder_api.views import Genres
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'genres', Genres, 'genre')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
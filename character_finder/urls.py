from character_finder_api.views.author import Authors
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from character_finder_api.views import Genres, SeriesView, Characters, Fictions

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'genres', Genres, 'genre')
router.register(r'series', SeriesView, 'series')
router.register(r'characters', Characters, 'character')
router.register(r'authors', Authors, 'author')
router.register(r'fictions', Fictions, 'fictionf')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
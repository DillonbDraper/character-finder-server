from character_finder_api.models.series import Series
from character_finder_api.views import Genres, SeriesView
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'genres', Genres, 'genre')
router.register(r'series', SeriesView, 'series')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
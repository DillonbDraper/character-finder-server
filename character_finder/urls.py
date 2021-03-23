from character_finder_api.views.author import Authors
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from character_finder_api.views import Genres, SeriesView, Characters, Fictions
from character_finder_api.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'genres', Genres, 'genre')
router.register(r'series', SeriesView, 'series')
router.register(r'characters', Characters, 'character')
router.register(r'authors', Authors, 'author')
router.register(r'fictions', Fictions, 'fiction')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

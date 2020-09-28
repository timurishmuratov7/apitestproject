from rest_framework import routers

from mainapp.views import AlbumViewSet
from registration.views import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('auth', AuthViewSet, basename='auth')
router.register('album', AlbumViewSet, basename='album')

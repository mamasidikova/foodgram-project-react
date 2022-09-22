from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router = DefaultRouter()

router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    url('', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
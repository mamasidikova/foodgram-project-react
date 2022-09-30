from django.conf.urls import url
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import SubscribeAPIView, SubscriptionsList, UserViewSet

router = DefaultRouter()

router.register('users', UserViewSet)


urlpatterns = [
    path('users/<int:id>/subscribe/', SubscribeAPIView.as_view()),
    path('users/subscriptions/', SubscriptionsList.as_view({'get': 'list'}),
         name='subscription'
         ),
    url('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

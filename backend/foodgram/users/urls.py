from django.conf.urls import url
from django.urls import include, re_path, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SubscribeAPIView, SubscriptionsList

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

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow, User
from .serializers import AddDeleteSubscriptionSerializer, CustomUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionsList(viewsets.ModelViewSet):
    serializer_class = AddDeleteSubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)


class SubscribeAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        subscription = get_object_or_404(Follow, user=user,
                                         author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        Follow.objects.get_or_create(user=user, author=author)
        serializer = AddDeleteSubscriptionSerializer(author,
                                                     context={
                                                         'request': request
                                                     })
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import User
from .serializers import CustomUserSerializer
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny, ]

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)




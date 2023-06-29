from rest_framework import viewsets, mixins

from api.bases.users.models import User
from api.versioned.v1.users.serializers import UserSerializer

from common.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)


class UserViewSet(ListModelMixin,
                  CreateModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  viewsets.GenericViewSet):
    """"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

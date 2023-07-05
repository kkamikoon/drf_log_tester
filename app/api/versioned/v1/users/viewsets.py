from rest_framework import viewsets

from app.api.bases.users.models import User
from app.api.versioned.v1.users.serializers import UserSerializer, UserRetrieveSerializer

from app.common.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    MappingViewSetMixin
)


class UserViewSet(ListModelMixin,
                  CreateModelMixin,
                  RetrieveModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  MappingViewSetMixin,
                  viewsets.GenericViewSet):
    """"""
    serializer_class = UserSerializer
    serializer_action_map = {
        "retrieve": UserRetrieveSerializer
    }
    queryset = User.objects.all()

from rest_framework import serializers
from api.bases.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", 'email', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
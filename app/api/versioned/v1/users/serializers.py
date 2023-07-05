from rest_framework import serializers
from app.api.bases.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ('id', 'last_login', 'date_joined', 'last_password_change', 'groups',
                            'user_permissions', 'is_online', )


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", 'email', 'is_staff', 'is_superuser', 'date_joined', 'last_login', )

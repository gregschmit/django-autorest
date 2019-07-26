"""
This module implements an example ``ViewSet``. I chose to do it for the ``User``
model because when you are creating a ``User``, you need to take a password and
a password confirmation, and even if you don't take a password confirmation, you
need to salt/hash the password prior to storing it, so it's a bit more complex
than just serializing some fields.
"""

from django.contrib.auth.models import User
from rest_framework.serializers import CharField, ModelSerializer, ValidationError
from rest_framework.viewsets import ModelViewSet


class UserSerializer(ModelSerializer):
    """
    An example serializer for the Django ``User`` model.
    """
    password_first = CharField(label='Password', write_only=True, required=False)
    password_confirmation = CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_first',
            'password_confirmation', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser', 'last_login',
            'date_joined', 'groups', 'user_permissions')
        extra_kwargs = {
            'password': {'read_only': True},
        }

    def get_password(self, validated_data, required=True):
        pw = validated_data.pop('password_first', None)
        pw_confirm = validated_data.pop('password_confirmation', None)
        if not pw:
            if required:
                raise ValidationError("A password must be provided!")
            else:
                return None
        if pw != pw_confirm:
            raise ValidationError("Passwords must match!")
        return pw

    def create(self, validated_data):
        pw = self.get_password(validated_data)
        superuser = validated_data.pop('is_superuser', None)
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        if superuser:
            u = User.objects.create_superuser(password=pw, **validated_data)
        else:
            u = User.objects.create_user(password=pw, **validated_data)
        u.groups.set(groups)
        u.user_permissions.set(user_permissions)
        return u


class UserDetailSerializer(UserSerializer):
    """
    An example serializer for the Django ``User`` model with details.
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_first',
            'password_confirmation', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser', 'last_login',
            'date_joined', 'groups', 'user_permissions')
        extra_kwargs = {
            'password': {'read_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
        }

    def update(self, instance, validated_data):
        pw = self.get_password(validated_data, required=False)
        if pw:
            instance.set_password(pw)
        return super().update(instance, validated_data)


class UserViewSet(ModelViewSet):
    """
    An example viewset for the Django ``User`` model.
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'create', 'destroy'):
            return UserSerializer
        elif self.action in ('retrieve', 'update', 'partial_update'):
            return UserDetailSerializer
        return None

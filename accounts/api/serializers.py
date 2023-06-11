from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from accounts.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(ModelSerializer):
    def validate(self, attrs):
        password = attrs.get('password')

        if len(password) < 6 or not any(char.isalnum() for char in password):
            raise ValidationError(
                'Password must be at least 6 characters long and contain at least one alphanumeric character.'
            )
        return attrs

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

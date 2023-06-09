from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from accounts.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'last_login']

    #TODO: validate password

    # def validate(self, value):
    #     password = value.get('password')

    #     if len(password) < 6 or not any(char.isalnum() for char in value):
    #         raise ValidationError(
    #             'Password must be at least 6 characters long and contain at least one alphanumeric character.'
    #         )
    #     return password
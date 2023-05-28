from rest_framework.serializers import ModelSerializer, ReadOnlyField
from accounts.models import Reviewer, User

class ReviewerSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.username')

    class Meta:
        model = Reviewer
        fields = ['user', 'display_name', 'bio']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'last_login']
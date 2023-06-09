from rest_framework.serializers import ModelSerializer, ReadOnlyField
from posts.models import Review

class ReviewSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = '__all__'

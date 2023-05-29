from rest_framework.serializers import ModelSerializer, ReadOnlyField
from reviews.models import Review

class ReviewSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = '__all__'

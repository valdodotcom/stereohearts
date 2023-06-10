from rest_framework.serializers import ModelSerializer, ReadOnlyField
from posts.models import Review, MusicList

class ReviewSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = '__all__'

class CreateReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class MusicListSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.username')

    class Meta:
        model = MusicList
        fields = '__all__'

class CreateListSerializer(ModelSerializer):
    class Meta:
        model = MusicList
        fields = '__all__'
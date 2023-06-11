from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from posts.models import Review, MusicList
from rest_framework.response import Response

class ReviewSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.username')

    def validate(self, attrs):
        is_liked = attrs.get('is_liked', False)
        is_disliked = attrs.get('is_disliked', False)

        if is_liked and is_disliked:
            raise ValidationError("A project cannot be liked and disliked at the same time.")
        return attrs

    class Meta:
        model = Review
        fields = '__all__'

class ListSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.username')

    def validate(self, attrs):
        is_liked = attrs.get('is_liked', False)
        is_disliked = attrs.get('is_disliked', False)

        if is_liked and is_disliked:
            raise ValidationError("A list cannot be liked and disliked at the same time.")
        return attrs

    class Meta:
        model = MusicList
        fields = '__all__'
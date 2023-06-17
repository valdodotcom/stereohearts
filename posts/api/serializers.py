from rest_framework import serializers
from posts.models import Review, MusicList

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.HyperlinkedIdentityField(view_name="posts:review-detail", lookup_field="pk")

    def validate(self, attrs):
        is_liked = attrs.get('is_liked', False)
        is_disliked = attrs.get('is_disliked', False)

        if is_liked and is_disliked:
            raise serializers.ValidationError("A project cannot be liked and disliked at the same time.")
        return attrs

    class Meta:
        model = Review
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.HyperlinkedIdentityField(view_name="posts:list-detail", lookup_field="pk")

    def validate(self, attrs):
        is_liked = attrs.get('is_liked', False)
        is_disliked = attrs.get('is_disliked', False)

        if is_liked and is_disliked:
            raise serializers.ValidationError("A list cannot be liked and disliked at the same time.")
        return attrs

    class Meta:
        model = MusicList
        fields = '__all__'
from rest_framework import serializers
from posts.models import *

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.HyperlinkedIdentityField(view_name="posts:review-detail", lookup_field="pk")
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    favourite_count = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    def get_project(self, obj):
        return {'title': obj.project.title, 'artist': obj.project.artist.name}

    def get_upvote_count(self, obj):
        return obj.upvotes.count()

    def get_downvote_count(self, obj):
        return obj.downvotes.count()
    
    def get_favourite_count(self, obj):
        return obj.favourites.count()

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
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    favourite_count = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()

    def get_projects(self, obj):
        return [{'title': project.title, 'artist': project.artist.name} for project in obj.projects.all()]

    def get_upvote_count(self, obj):
        return obj.upvotes.count()

    def get_downvote_count(self, obj):
        return obj.downvotes.count()
    
    def get_favourite_count(self, obj):
        return obj.favourites.count()

    def validate(self, attrs):
        is_liked = attrs.get('is_liked', False)
        is_disliked = attrs.get('is_disliked', False)

        if is_liked and is_disliked:
            raise serializers.ValidationError("A list cannot be liked and disliked at the same time.")
        return attrs

    class Meta:
        model = MusicList
        fields = '__all__'

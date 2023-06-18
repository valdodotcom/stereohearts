from rest_framework import serializers
from posts.models import *
from .mixins import PostSerializerMixin

class ReviewSerializer(PostSerializerMixin, serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.HyperlinkedIdentityField(view_name="posts:review-detail", lookup_field="pk")
    project_info = serializers.SerializerMethodField()

    def get_project_info(self, obj):
        return {'title': obj.project.title, 'artist': obj.project.artist.name}

    class Meta:
        model = Review
        fields = '__all__'



class ListSerializer(PostSerializerMixin, serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.HyperlinkedIdentityField(view_name="posts:list-detail", lookup_field="pk")
    projects_info = serializers.SerializerMethodField()

    def get_projects_info(self, obj):
        return [{'title': project.title, 'artist': project.artist.name} for project in obj.projects.all()]

    class Meta:
        model = MusicList
        fields = '__all__'

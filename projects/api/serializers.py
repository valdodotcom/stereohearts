from rest_framework import serializers
from projects.models import Project, Artist

class ProjectSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name="projects:project-detail", lookup_field="pk")

    class Meta:
        model = Project
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name="projects:artist-detail", lookup_field="pk")

    class Meta:
        model = Artist
        fields = '__all__'
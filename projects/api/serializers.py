from rest_framework import serializers
from projects.models import Project, Artist
from rest_framework.reverse import reverse

class ProjectSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name="projects:project-detail", lookup_field="pk")
    artist_name = serializers.ReadOnlyField(source='artist.name')
    artist_url = serializers.SerializerMethodField()

    def get_artist_url(self, obj):
        request = self.context.get('request')
        return reverse('projects:artist-detail', kwargs={'pk': obj.artist.id}, request=request)

    class Meta:
        model = Project
        exclude = ['artist']

class ArtistSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name="projects:artist-detail", lookup_field="pk")
    projects = serializers.SerializerMethodField()

    def get_projects(self, obj):
        projects = obj.projects.filter(artist=obj.id)
        request = self.context.get('request')
        return [
            {
                'title': project.title,
                'url': reverse('projects:project-detail', kwargs={'pk': project.id}, request=request)
            }
                for project in projects
        ]

    class Meta:
        model = Artist
        fields = '__all__'
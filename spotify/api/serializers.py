from rest_framework import serializers
from rest_framework.reverse import reverse
from urllib.parse import urlencode

class ArtistSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

class ParsedAlbumSerializer(serializers.Serializer):
    id = serializers.CharField()
    added_at = serializers.DateTimeField()
    album_type = serializers.CharField()
    artists = ArtistSerializer(many=True)
    external_urls = serializers.DictField()
    name = serializers.CharField()
    release_date = serializers.DateField()
    total_tracks = serializers.IntegerField()
    tracks = serializers.ListField()
    create_review = serializers.SerializerMethodField()
    add_to_list = serializers.SerializerMethodField()
    image = serializers.CharField()

    def get_create_review(self, obj):
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            # Construct the URL for creating a review
            url = reverse('posts:create-review')
            params = {
                'project': obj['id'],
            }
            return f"{request.build_absolute_uri(url)}?{urlencode(params)}"

        return None
    
    def get_add_to_list(self, obj):
        request = self.context.get('request')
        if request is not None and request.user.is_authenticated:
            url = reverse('posts:add-to-list')
            params = {
                'project': obj['id'],
            }
            return f"{request.build_absolute_uri(url)}?{urlencode(params)}"

        return None
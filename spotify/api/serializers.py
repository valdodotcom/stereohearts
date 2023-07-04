from rest_framework import serializers

class ArtistSerializer(serializers.Serializer):
    external_urls = serializers.DictField()
    artist_name = serializers.CharField()

class ParsedAlbumSerializer(serializers.Serializer):
    added_at = serializers.DateTimeField()
    album_type = serializers.CharField()
    artists = ArtistSerializer(many=True)
    external_urls = serializers.DictField()
    album_name = serializers.CharField()
    release_date = serializers.DateField()
    total_tracks = serializers.IntegerField()
    tracks = serializers.ListField()
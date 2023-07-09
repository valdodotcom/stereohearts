from rest_framework import serializers
from posts.models import *
from .mixins import PostSerializerMixin
from rest_framework.reverse import reverse
import requests
from spotify.util import is_spotify_authenticated, get_user_tokens


class ReviewSerializer(PostSerializerMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="posts:review-detail", lookup_field="pk")
    vote_url = serializers.HyperlinkedIdentityField(view_name="posts:review-vote", lookup_field="pk")
    new_comment_url = serializers.HyperlinkedIdentityField(view_name="posts:review-comment", lookup_field="pk")
    project_info = serializers.SerializerMethodField()
    comm_url = "posts:review-comment-vote"

    def get_project_info(self, obj):
        # Get the album ID or other necessary information from the review object or any other source
        album = obj.project

        # Make a request to the Spotify API
        session_key = self.context['request'].session.session_key
        is_authenticated = is_spotify_authenticated(self.context['request'].user, session_key)

        if is_authenticated:
            user_tokens = get_user_tokens(session_key)
            access_token = user_tokens.access_token

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            album_endpoint = f'https://api.spotify.com/v1/albums/{album}'
            response = requests.get(album_endpoint, headers=headers)

            if response.status_code == 200:
                data = response.json()

                artists = data.get('artists', [])
                artist_info = [
                    {
                        'name': artist.get('name'),
                        'url': artist.get('external_urls', {}).get('spotify')
                    }
                    for artist in artists
                ]

                album_info = {
                    'album_type': data.get('album_type'),
                    'artists': artist_info,
                    'url': data.get('external_urls', {}).get('spotify'),
                    'name': data.get('name'),
                    'release_date': data.get('release_date'),
                    'total_tracks': data.get('total_tracks'),
                    'tracks': [track['name'] for track in data.get('tracks', {}).get('items')]
                }

                return album_info
        # print(response.json())
        return None
    
    class Meta:
        model = Review
        fields = '__all__'

        # exclude = ['project']

class ReviewVoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    review = serializers.ReadOnlyField(source='review.title')

    class Meta:
        model = ReviewVote
        fields = '__all__'

class ReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    review = serializers.ReadOnlyField(source='review.title')

    class Meta:
        model = ReviewComment
        fields = '__all__'

class ReviewCommentVoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    review_comment = serializers.ReadOnlyField(source='review_comment.id')

    class Meta:
        model = ReviewCommentVote
        fields = '__all__'


class ListSerializer(PostSerializerMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="posts:list-detail", lookup_field="pk")
    vote_url = serializers.HyperlinkedIdentityField(view_name="posts:list-vote", lookup_field="pk")
    new_comment_url = serializers.HyperlinkedIdentityField(view_name="posts:list-comment", lookup_field="pk")
    # projects = serializers.SerializerMethodField()
    projects_info = serializers.SerializerMethodField()
    comm_url = "posts:list-comment-vote"

    def get_projects(self, obj):
        projects = obj.get_projects_list()
        return projects

    def get_projects_info(self, obj):
        projects = obj.get_projects_list()
        projects_info = []

        session_key = self.context['request'].session.session_key
        is_authenticated = is_spotify_authenticated(self.context['request'].user, session_key)

        if is_authenticated:
            user_tokens = get_user_tokens(session_key)
            access_token = user_tokens.access_token

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            for project in projects:
                album_endpoint = f'https://api.spotify.com/v1/albums/{project}'
                response = requests.get(album_endpoint, headers=headers)

                if response.status_code == 200:
                    data = response.json()

                    artists = data.get('artists', [])
                    artist_info = [
                        {
                            'name': artist.get('name'),
                            'url': artist.get('external_urls', {}).get('spotify')
                        }
                        for artist in artists
                    ]

                    album_info = {
                        'album_type': data.get('album_type'),
                        'artists': artist_info,
                        'url': data.get('external_urls', {}).get('spotify'),
                        'name': data.get('name'),
                        'release_date': data.get('release_date'),
                        'total_tracks': data.get('total_tracks'),
                        'tracks': [track['name'] for track in data.get('tracks', {}).get('items')]
                    }

                    projects_info.append(album_info)

        # print(response.json())
        return projects_info

    class Meta:
        model = MusicList
        fields = '__all__'
        # exclude = ['projects']

class ListVoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    music_list = serializers.ReadOnlyField(source='music_list.title')

    class Meta:
        model = ListVote
        fields = '__all__'

class ListCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    music_list = serializers.ReadOnlyField(source='music_list.title')

    class Meta:
        model = ListComment
        fields = '__all__'

class ListCommentVoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    list_comment = serializers.ReadOnlyField(source='list_comment.id')

    class Meta:
        model = ListCommentVote
        fields = '__all__'
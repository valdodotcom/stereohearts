from os import environ
from dotenv import load_dotenv

from django.shortcuts import redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from spotify.util import update_or_create_user_tokens, is_spotify_authenticated, get_user_tokens
from spotify.api.serializers import *
import requests

load_dotenv()
SPOTIFY_URL = environ.get('SPOTIFY_URL')
REDIRECT_URI = environ.get('SPOTIFY_REDIRECT_URI')
CLIENT_ID = environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = environ.get('SPOTIFY_CLIENT_SECRET')

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /spotify',
        'GET /spotify/auth', 
        'GET /spotify/redirect',
        'GET /spotify/is-authenticated'
    ]

    return Response(routes) 

@api_view(['GET'])
def getAuth(request):
    endpoint = SPOTIFY_URL + 'authorize'
    scopes = 'user-library-read user-follow-read'

    parameters = {'scope': scopes,
                'response_type': 'code',
                'redirect_uri': REDIRECT_URI,
                'client_id': CLIENT_ID}
    
    url = Request('GET', endpoint, params=parameters).prepare().url
    return Response({'url': url}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getCallback(request):
    endpoint = SPOTIFY_URL + 'api/token'
    code = request.GET.get('code')
    error = request.GET.get('error')

    callback_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = post(endpoint, data=callback_data).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(request.user,
        request.session.session_key, access_token, refresh_token,
        token_type, expires_in)

    # TODO: Change redirect to frontend home:
    return redirect('spotify:library')

@api_view(['GET'])
def getIsAuthenticated(self, request):
    is_authenticated = is_spotify_authenticated(self.request.user, request.session.session_key)
    return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


class SpotifyLibraryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SpotifyLibraryView(ListAPIView):
    pagination_class = SpotifyLibraryPagination
    serializer_class = ParsedAlbumSerializer
    
    def get_queryset(self):
        session_key = self.request.session.session_key
        is_authenticated = is_spotify_authenticated(self.request.user, session_key)

        if is_authenticated:
            user_tokens = get_user_tokens(session_key)
            access_token = user_tokens.access_token

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            # Fetch the library data using Spotify's API
            params = {'limit': 50, 'offset': 0}
            library_endpoint = 'https://api.spotify.com/v1/me/albums'

            response = requests.get(library_endpoint, headers=headers, params=params)
            if response.status_code == 200:
                library_data = response.json()
                albums = library_data.get('items')
                parsed_albums = []

                for album in albums:
                    artists = album.get('album', {}).get('artists', [])
                    tracks = album.get('album', {}).get('tracks', []).get('items', [])

                    parsed_artists = []
                    track_names = []

                    for artist in artists:
                        parsed_artist = {
                            'id': artist.get('id'),
                            'name': artist.get('name'),
                        }
                        parsed_artists.append(parsed_artist)

                    for track in tracks:
                        track_name = track.get('name')
                        track_names.append(track_name)


                    parsed_album = {
                        'added_at': album.get('added_at'),
                        'id': album.get('album', {}).get('id'),
                        'album_type': album.get('album', {}).get('album_type'),
                        'artists': parsed_artists,
                        'external_urls': album.get('album', {}).get('external_urls'),
                        'name': album.get('album', {}).get('name'),
                        'release_date': album.get('album', {}).get('release_date'),
                        'total_tracks': album.get('album', {}).get('total_tracks'),
                        'tracks': track_names,
                    }
                    parsed_albums.append(parsed_album)

                return parsed_albums

        return []

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
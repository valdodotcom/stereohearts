from os import environ
from dotenv import load_dotenv

from django.shortcuts import redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post
from rest_framework.generics import ListAPIView

from spotify.util import update_or_create_user_tokens, is_spotify_authenticated, get_user_tokens
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
    print(response)

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
def getIsAuthenticated(request):
    is_authenticated = is_spotify_authenticated(request.session.session_key)
    return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


class SpotifyLibraryView(ListAPIView):
    def get_queryset(self):
        session_key = self.request.session.session_key
        is_authenticated = is_spotify_authenticated(session_key)

        if is_authenticated:
            user_tokens = get_user_tokens(session_key)
            access_token = user_tokens.access_token

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            # Fetch the library data using Spotify's API
            library_endpoint = 'https://api.spotify.com/v1/me/tracks'
            response = requests.get(library_endpoint, headers=headers)
            if response.status_code == 200:
                library_data = response.json()
                tracks = library_data.get('items')
                return tracks

        return []

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset, status=status.HTTP_200_OK)
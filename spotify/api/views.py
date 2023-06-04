from os import environ
from dotenv import load_dotenv

from django.shortcuts import redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post

from spotify.util import update_or_create_user_tokens, is_spotify_authenticated

load_dotenv()
SPOTIFY_URL = environ.get('SPOTIFY_URL')
REDIRECT_URI = environ.get('REDIRECT_URI')
CLIENT_ID = environ.get('CLIENT_ID')
CLIENT_SECRET = environ.get('CLIENT_SECRET')

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /spotify',
        'GET /spotify/auth', 
        'GET /spotify/redirect',
        'GET /spotify/is-authenticated'
        # 'GET /reviews/view/:username',
        # 'POST /reviews/create',
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

    update_or_create_user_tokens(
        request.session.session_key, access_token, refresh_token,
        token_type, expires_in)

    # TODO: Change redirect to frontend:
    return redirect('accounts:')

@api_view(['GET'])
def getIsAuthenticated(self, request):
    is_authenticated = is_spotify_authenticated(self.request.session.session_key)
    return Response({'status': is_authenticated}, status=status.HTTP_200_OK)

from .models import SpotifyToken

from django.utils import timezone
from rest_framework.response import Response

from datetime import timedelta
import requests
import base64

from os import environ
from dotenv import load_dotenv
load_dotenv()

SPOTIFY_URL = environ.get('SPOTIFY_URL')
CLIENT_ID = environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = environ.get('SPOTIFY_CLIENT_SECRET')

def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(spotify_user=session_id)
    if user_tokens.exists():
        return user_tokens[0]


def update_or_create_user_tokens(user, session_id, access_token, 
                                  refresh_token, token_type, expires_in):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=3600)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 
                                   'token_type', 'expires_in'])

    else:
        tokens = SpotifyToken(user=user, spotify_user=session_id, access_token=access_token, 
                              refresh_token=refresh_token, token_type=token_type, 
                              expires_in=expires_in)
        tokens.save()

def is_spotify_authenticated(user, session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(user, session_id)
            
        return True
    
    return False

def refresh_spotify_token(user, session_id):
    refresh_token = get_user_tokens(session_id).refresh_token
    auth_client = CLIENT_ID + ":" + CLIENT_SECRET
    auth_encode = 'Basic ' + base64.b64encode(auth_client.encode()).decode()

    headers = { 'Authorization': auth_encode }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        }

    response = requests.post(SPOTIFY_URL+'api/token', data=data, headers=headers)
    if(response.status_code == 200):
        response_json = response.json()
        access_token = response_json["access_token"]
        token_type = response_json["token_type"]
        expires_in = response_json["expires_in"]

        update_or_create_user_tokens(
            user, session_id, access_token, refresh_token, token_type, expires_in)
        
    else:
        return Response({'error': 'could not refresh token'}, status=400)
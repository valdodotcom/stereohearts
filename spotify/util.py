from .models import SpotifyToken

from django.utils import timezone

from datetime import timedelta
from requests import post

from os import environ
from dotenv import load_dotenv
load_dotenv()

SPOTIFY_URL = environ.get('SPOTIFY_URL')

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

def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
            
        return True
    
    return False

def refresh_spotify_token(user, session_id):
    refresh_token = get_user_tokens(session_id).refresh_token
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': environ.get('CLIENT_ID'),
        'client_secret': environ.get('CLIENT_SECRET')
    }
    response = post(SPOTIFY_URL+'/api/token', data=data).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(
        user, session_id, access_token, refresh_token, token_type, expires_in)
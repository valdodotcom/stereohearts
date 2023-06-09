from django.db import models

# Create your models here.
from accounts.models import User
class SpotifyToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #changed from Reviewer to User
    spotify_user = models.CharField(max_length=50, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150,  null=True)
    access_token = models.CharField(max_length=150, null=True)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50, null=True)
from django.db import models

# Create your models here.
from accounts.models import Reviewer
class SpotifyToken(models.Model):
    user = models.ForeignKey(Reviewer, on_delete=models.CASCADE)
    spotify_user = models.CharField(max_length=50, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150,  null=True)
    access_token = models.CharField(max_length=150, null=True)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50, null=True)
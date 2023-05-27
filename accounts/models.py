from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  email = models.EmailField(unique=True, null=True)

class Reviewer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  name = models.CharField(max_length=200, null=True)
  bio = models.TextField(blank=True, null=True)
  # profile_picture = models.ImageField(upload_to='reviewer_profiles/', blank=True)
  # reviews = models.ManyToManyField(ReviewModel, related_name='reviewers')
  # favorite_project = models.ManyToManyField('Project', related_name='reviewers')
  # favorite_artists = models.ManyToManyField('Artist', related_name='reviewers')
  def __str__(self):
    return self.username

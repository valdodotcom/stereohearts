from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  email = models.EmailField(unique=True, null=False)

  #assuming the vast majority of users will be reviewers
  is_reviewer = models.BooleanField(default=True)
  is_moderator = models.BooleanField(default=False)

  #I'll leave you to add any more fields you want, especially those from the Reviewer class below  
  
  def __str__(self):
    return self.username

# class Reviewer(models.Model):

#   user = models.ForeignKey(User, on_delete=models.CASCADE)
#   display_name = models.CharField(max_length=200, null=True)
#   bio = models.TextField(blank=True, null=True)
#   # profile_picture = models.ImageField(upload_to='reviewer_profiles/', blank=True)
#   # reviews = models.OneToManyField(Review, related_name='reviewers')
#   # lists = models.OneToManyField(List, related_name='reviewers')
#   # likes =  models.OneToManyField(Like, related_name='reviewers')
#   # favorite_project = models.ManyToManyField('Project', related_name='reviewers')
#   # favorite_artists = models.ManyToManyField('Artist', related_name='reviewers')
#   # score = models.CharField(max_length=200, null=True)

#   def __str__(self):
#     return self.user.username

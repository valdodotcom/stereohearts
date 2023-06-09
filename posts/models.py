from django.db import models

# Create your models here.
from accounts.models import User
from django.core.validators import MinValueValidator as min, MaxLengthValidator as max
from django.core.exceptions import ValidationError

class Review(models.Model):
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        # validators=[min(0), max(100)]
        )
    title = models.CharField(max_length=100, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)

    # def clean(self):
    #     if self.is_liked and self.is_disliked:
    #         raise ValidationError("A project cannot be liked and disliked at the same time.")

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    #     return f"{self.project.title} - {self.project.artist}: {self.user.username}"

class MusicList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

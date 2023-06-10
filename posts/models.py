from django.db import models

# Create your models here.
from accounts.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# validator functions
def validate_rating(value):
    if value < 0 or value > 100:
        raise ValidationError(
            _("%(value)s is not a valid rating. Value must range from 0 to 100"),
            params={"value": value},)
    
class Review(models.Model):
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[validate_rating])
    title = models.CharField(max_length=100, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)

    def clean(self):
        if self.is_liked and self.is_disliked:
            raise ValidationError("A project cannot be liked and disliked at the same time.")

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

    def clean(self):
        if self.is_liked and self.is_disliked:
            raise ValidationError("A list cannot be liked and disliked at the same time.")

    def __str__(self):
        return f"{self.user.username} - {self.title}"

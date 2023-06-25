from django.db import models

# Create your models here.
from accounts.models import User
from projects.models import Project

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# validator functions
def validate_rating(value):
    if value < 0 or value > 100:
        raise ValidationError(
            _("%(value)s is not a valid rating. Value must range from 0 to 100"),
            params={"value": value},)
    

class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
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


class ReviewUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_upvotes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.review.title}"


class ReviewDownvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_downvotes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='downvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} dislikes {self.review.title}"


class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.title}"


class ReviewFavourite(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_favourites')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} favourited {self.review.title}"


class MusicList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='music_lists')
    projects = models.ManyToManyField(Project, related_name='music_lists')
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
    
    def get_projects_list(self):
        return list(self.projects.all())

class ListUpvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_upvotes')
    music_list = models.ForeignKey(MusicList, on_delete=models.CASCADE, related_name='upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.music_list.title}"


class ListDownvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_downvotes')
    music_list = models.ForeignKey(MusicList, on_delete=models.CASCADE, related_name='downvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} dislikes {self.music_list.title}"


class ListComment(models.Model):
    music_list = models.ForeignKey(MusicList, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.music_list.title}"


class ListFavourite(models.Model):
    music_list = models.ForeignKey(MusicList, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_favourites')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} favourited {self.music_list.title}"

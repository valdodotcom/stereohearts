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
    
def validate_like_dislike(value):
    if value < -1 or value > 1:
        raise ValidationError(
            _("%(value)s is not a valid input. Value must be -1, 0 or 1"),
            params={"value": value},)
    

class Review(models.Model):
    project = models.CharField(max_length=100, default='item1')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[validate_rating], null=True)
    title = models.CharField(max_length=100, null=True)
    body = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like_dislike = models.IntegerField(default=0, validators=[validate_like_dislike])

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class ReviewVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_votes')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
    status = models.IntegerField(default=0, validators=[validate_like_dislike])
    is_fav = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        if self.status == 0:
            return f"{self.user.username} removed vote on review '{self.review.title}'"
        
        if self.status == 1:
            return f"{self.user.username} likes review '{self.review.title}'"
        
        if self.status == -1:
            return f"{self.user.username} dislikes review '{self.review.title}'"


class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented '{self.body}' on review '{self.review.title}'"


class ReviewCommentVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_comment_votes')
    review_comment = models.ForeignKey(ReviewComment, on_delete=models.CASCADE, related_name='comment_votes')
    status = models.IntegerField(default=0, validators=[validate_like_dislike])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review_comment')

    def __str__(self):
        if self.status == 0:
            return f"{self.user.username} removed vote on comment '{self.review_comment.body}'"
        
        if self.status == 1:
            return f"{self.user.username} likes comment '{self.review_comment.body}'"
        
        if self.status == -1:
            return f"{self.user.username} dislikes comment '{self.review_comment.body}'"


class MusicList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='music_lists')
    projects = models.CharField(max_length=1100, default="item1,item2")  # Storing project IDs as a comma-separated string
    title = models.CharField(max_length=100, null=True)
    body = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like_dislike = models.IntegerField(default=0, validators=[validate_like_dislike])

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def get_projects_list(self):
        return self.projects.split(',')
    
    def get_projects_str(self):
        projects = self.projects.split(',')
        return [str(project) for project in projects]


class ListVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_votes')
    music_list = models.ForeignKey(MusicList, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0, validators=[validate_like_dislike])
    is_fav = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'music_list')

    def __str__(self):
        if self.status == 0:
            return f"{self.user.username} removed vote on list '{self.music_list.title}'"
        
        if self.status == 1:
            return f"{self.user.username} likes list '{self.music_list.title}'"
        
        if self.status == -1:
            return f"{self.user.username} dislikes list '{self.music_list.title}'"


class ListComment(models.Model):
    music_list = models.ForeignKey(MusicList, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented '{self.body}' on list '{self.music_list.title}'"
    

class ListCommentVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_comment_votes')
    list_comment = models.ForeignKey(ListComment, on_delete=models.CASCADE, related_name='comment_votes')
    status = models.IntegerField(default=0, validators=[validate_like_dislike])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'list_comment')

    def __str__(self):
        if self.status == 0:
            return f"{self.user.username} removed vote on comment '{self.list_comment.body}'"
        
        if self.status == 1:
            return f"{self.user.username} likes comment '{self.list_comment.body}'"
        
        if self.status == -1:
            return f"{self.user.username} dislikes comment '{self.list_comment.body}'"

from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from accounts.models import User
from rest_framework.reverse import reverse

class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    reviews = serializers.SerializerMethodField()
    music_lists = serializers.SerializerMethodField()
    activity = serializers.SerializerMethodField()
    follow_url = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        reviews = obj.reviews.prefetch_related('project')
        request = self.context.get('request')
        return [{'title': str(review.title), 
                 'project': str(review.project), 
                 'url': reverse('posts:review-detail', 
                                args=[review.pk], request=request)} for review in reviews]
    
    def get_music_lists(self, obj):
        music_lists = obj.music_lists.prefetch_related('projects')
        request = self.context.get('request')
        return [{'title': str(music_list.title), 
                 'projects': music_list.get_projects_str(), 
                 'url': reverse('posts:list-detail', 
                                args=[music_list.pk], request=request)} for music_list in music_lists]
    
    def get_activity(self, obj):
        list_votes = list(obj.list_votes.all())
        review_votes = list(obj.review_votes.all())  
        review_comments = list(obj.review_comments.all())
        list_comments = list(obj.list_comments.all())
        # list_favs = list(obj.list_votes.filter(is_fav=True))
        combined_votes = list_votes + review_votes + review_comments + list_comments
        # filtered_votes = [str(vote) for vote in combined_votes if vote.status != 0]
        filtered_votes = [str(vote) for vote in combined_votes]
        return filtered_votes[:5]
    
    def get_following(self, obj):
        following = obj.following.all()
        return [user.username for user in following]

    def get_followers(self, obj):
        followers = obj.followers.all()
        return [user.username for user in followers]
    
    def get_follow_url(self, obj):
        request = self.context.get('request')
        return reverse('accounts:follow', args=[obj.pk], request=request)


    def validate(self, attrs):
        password = attrs.get('password')

        if len(password) < 6 or not any(char.isalnum() for char in password):
            raise ValidationError(
                'Password must be at least 6 characters long and contain at least one alphanumeric character.'
            )
        return attrs

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'display_name', 'bio', 'reviews', 'music_lists',
                  'activity', 'following', 'followers', 'follow_url',
                  ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
        }
from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from rest_framework import serializers
from accounts.models import User
from posts.models import Review
from django.contrib.auth.hashers import make_password
from rest_framework.reverse import reverse

class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    reviews = serializers.SerializerMethodField()
    music_lists = serializers.SerializerMethodField()

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
                  'display_name', 'bio', 'reviews', 'music_lists']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
        }
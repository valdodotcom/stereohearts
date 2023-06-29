from rest_framework import serializers
from posts.models import *

class PostSerializerMixin(serializers.Serializer):
    user = serializers.ReadOnlyField(source='user.username')
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    favourites_count = serializers.SerializerMethodField()

    def get_upvotes(self, obj):
        return [vote.user.username for vote in obj.votes.filter(status=1)]

    def get_downvotes(self, obj):
        return [vote.user.username for vote in obj.votes.filter(status=-1)]
    
    def get_comments(self, obj):
        return [
            {
                'user': comment.user.username,
                'body': comment.body,
                'created_at': comment.created_at
            }
            for comment in obj.comments.all()
        ]
    
    def get_favourites_count(self, obj):
        return obj.votes.filter(is_fav=True).count()
    

class PostViewMixin:
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = self.model.objects.all().order_by('-created_at')

        if username:
            queryset = queryset.filter(user__username=username)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

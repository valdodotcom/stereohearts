from rest_framework import serializers
from posts.models import *

class PostSerializerMixin(serializers.Serializer):
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    favourites_count = serializers.SerializerMethodField()

    def get_upvote_count(self, obj):
        return obj.votes.filter(status=1).count()

    def get_downvote_count(self, obj):
        return obj.votes.filter(status=-1).count()
    
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

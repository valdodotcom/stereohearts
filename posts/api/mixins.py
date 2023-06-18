from rest_framework import serializers
from posts.models import *

class PostSerializerMixin(serializers.Serializer):
    upvote_count = serializers.SerializerMethodField()
    downvote_count = serializers.SerializerMethodField()
    favourite_count = serializers.SerializerMethodField()

    def get_upvote_count(self, obj):
        return obj.upvotes.count()

    def get_downvote_count(self, obj):
        return obj.downvotes.count()
    
    def get_favourite_count(self, obj):
        return obj.favourites.count()

    def validate(self, attrs):
        is_liked = attrs.get('is_liked', False)
        is_disliked = attrs.get('is_disliked', False)

        if is_liked and is_disliked:
            raise serializers.ValidationError(f"A {self.Meta.model.__name__.lower()} cannot be liked and disliked at the same time.")
        return attrs
    

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

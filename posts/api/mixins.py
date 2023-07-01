from rest_framework import serializers
from posts.models import *
from rest_framework.reverse import reverse

class PostSerializerMixin(serializers.Serializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_url = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='accounts:get-user',
        source='user',
        lookup_field='pk'
    )
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    favourites_count = serializers.SerializerMethodField()

    def get_upvotes(self, obj):
        request = self.context.get('request')
        return [
            {
                'user': vote.user.username,
                'user_url': reverse('accounts:get-user', kwargs={'pk': vote.user.id}, request=request),    
            }
                 for vote in obj.votes.filter(status=1)
        ]

    def get_downvotes(self, obj):
        request = self.context.get('request')
        return [
            {
                'user': vote.user.username,
                'user_url': reverse('accounts:get-user', kwargs={'pk': vote.user.id}, request=request),    
            }
                 for vote in obj.votes.filter(status=-1)
        ]
    
    def get_comments(self, obj):
        request = self.context.get('request')
        return [
            {
                'user': comment.user.username,
                'user_url': reverse('accounts:get-user', kwargs={'pk': comment.user.id}, request=request),
                'body': comment.body,
                'created_at': comment.created_at,
                'comment_url': reverse(self.comm_url, kwargs={'pk': comment.id}, request=request)
            }
            for comment in obj.comments.all().order_by('-created_at')
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
    

class PostVoteMixin:
    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset
    
    def perform_create(self, serializer, id_field):
        id = self.kwargs['pk']
        existing_vote = self.model.objects.filter(user=self.request.user, **{id_field: id}).first()
        if existing_vote:
            serializer.update(existing_vote, serializer.validated_data)
        else:
            serializer.save(user=self.request.user, **{id_field: id})


class PostCommentMixin:
    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset
    
    def perform_create(self, serializer, obj_field, parent_model):
        id = self.kwargs['pk']
        obj = parent_model.objects.get(pk=id)
        serializer.save(user=self.request.user, **{obj_field: obj})
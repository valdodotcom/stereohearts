from rest_framework import serializers
from posts.models import *
from .mixins import PostSerializerMixin
from rest_framework.reverse import reverse

class ReviewSerializer(PostSerializerMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="posts:review-detail", lookup_field="pk")
    vote_url = serializers.HyperlinkedIdentityField(view_name="posts:review-vote", lookup_field="pk")
    new_comment_url = serializers.HyperlinkedIdentityField(view_name="posts:review-comment", lookup_field="pk")
    project_info = serializers.SerializerMethodField()
    comm_url = "posts:review-comment-vote"

    def get_project_info(self, obj):
        request = self.context.get('request')
        return {
            'title': obj.project.title,
            'artist': obj.project.artist.name,
            'url': reverse('projects:project-detail', kwargs={'pk': obj.project.id}, request=request),
            }

    class Meta:
        model = Review
        exclude = ['project']

class ReviewVoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    review = serializers.ReadOnlyField(source='review.title')

    class Meta:
        model = ReviewVote
        fields = '__all__'

class ReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    review = serializers.ReadOnlyField(source='review.title')

    class Meta:
        model = ReviewComment
        fields = '__all__'

class ReviewCommentVoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    review_comment = serializers.ReadOnlyField(source='review_comment.id')

    class Meta:
        model = ReviewCommentVote
        fields = '__all__'


class ListSerializer(PostSerializerMixin, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="posts:list-detail", lookup_field="pk")
    vote_url = serializers.HyperlinkedIdentityField(view_name="posts:list-vote", lookup_field="pk")
    new_comment_url = serializers.HyperlinkedIdentityField(view_name="posts:list-comment", lookup_field="pk")
    projects_info = serializers.SerializerMethodField()
    comm_url = "posts:list-comment-vote"

    def get_projects_info(self, obj):
        request = self.context.get('request')
        return [
            {
                'title': project.title, 
                'artist': project.artist.name,
                'url': reverse('projects:project-detail', kwargs={'pk': project.id}, request=request),
            } 
            for project in obj.projects.all()
        ]

    class Meta:
        model = MusicList
        exclude = ['projects']

class ListVoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    music_list = serializers.ReadOnlyField(source='music_list.title')

    class Meta:
        model = ListVote
        fields = '__all__'

class ListCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    music_list = serializers.ReadOnlyField(source='music_list.title')

    class Meta:
        model = ListComment
        fields = '__all__'

class ListCommentVoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    list_comment = serializers.ReadOnlyField(source='list_comment.id')

    class Meta:
        model = ListCommentVote
        fields = '__all__'
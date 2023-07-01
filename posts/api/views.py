from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, MusicList
from .serializers import *
from .permissions import IsPostOwnerOrReadOnly
from .mixins import PostViewMixin, PostVoteMixin, PostCommentMixin
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /posts/',
        'GET /posts/reviews/',
        'GET /posts/reviews/?username=:username',
        'GET /posts/reviews/review_id',
        'GET /posts/lists/', 
        'GET /posts/lists/?username=:username',
        'GET /posts/lists/list_id',
    ]

    return Response(routes) 


class ReviewView(PostViewMixin, ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = Review

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsPostOwnerOrReadOnly]
    queryset = Review.objects.all()

class ReviewVoteView(PostVoteMixin ,CreateAPIView):
    serializer_class = ReviewVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ReviewVote

    def perform_create(self, serializer):
        super().perform_create(serializer, 'review_id')

class ReviewCommentView(PostCommentMixin, CreateAPIView):
    serializer_class = ReviewCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ReviewComment
    
    def perform_create(self, serializer):
        super().perform_create(serializer, 'review', Review)

class ReviewCommentVoteView(PostVoteMixin, CreateAPIView):
    serializer_class = ReviewCommentVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ReviewCommentVote

    def perform_create(self, serializer):
        super().perform_create(serializer, 'review_comment_id')

class ListView(PostViewMixin, ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = MusicList

class ListDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ListSerializer
    permission_classes = [IsPostOwnerOrReadOnly]
    queryset = MusicList.objects.all()

class ListVoteView(PostVoteMixin, CreateAPIView):
    serializer_class = ListVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ListVote

    def perform_create(self, serializer):
        super().perform_create(serializer, 'music_list_id')

class ListCommentView(PostCommentMixin, CreateAPIView):
    serializer_class = ListCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ListComment
    
    def perform_create(self, serializer):
        super().perform_create(serializer, 'music_list', MusicList)

class ListCommentVoteView(PostVoteMixin, CreateAPIView):
    serializer_class = ListCommentVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ListCommentVote

    def perform_create(self, serializer):
        super().perform_create(serializer, 'list_comment_id')
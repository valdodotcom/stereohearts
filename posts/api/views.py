from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, MusicList
from .serializers import *
from .permissions import IsPostOwnerOrReadOnly
from .mixins import PostViewMixin
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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsPostOwnerOrReadOnly]

class ReviewVoteView(CreateAPIView):
    queryset = ReviewVote.objects.all()
    serializer_class = ReviewVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        id = self.kwargs['pk']  # Get the review ID from URL parameter
        serializer.save(user=self.request.user, review_id=id)
        return super().perform_create(serializer)


class ReviewCommentView(CreateAPIView):
    queryset = ReviewComment.objects.all()
    serializer_class = ReviewCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        id = self.kwargs['pk']
        serializer.save(user=self.request.user, review_id=id)
        return super().perform_create(serializer)


class ListView(PostViewMixin, ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = MusicList

class ListDetailView(RetrieveUpdateDestroyAPIView):
    queryset = MusicList.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsPostOwnerOrReadOnly]

class ListVoteView(CreateAPIView):
    queryset = ListVote.objects.all()
    serializer_class = ListVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        id = self.kwargs['pk']  # Get the list ID from URL parameter
        obj = MusicList.objects.get(pk=id)
        serializer.save(user=self.request.user, music_list=obj)

class ListCommentView(CreateAPIView):
    queryset = ListComment.objects.all()
    serializer_class = ListCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        id = self.kwargs['pk']  # Get the list ID from URL parameter
        obj = MusicList.objects.get(pk=id)
        serializer.save(user=self.request.user, music_list=obj)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, MusicList
from .serializers import *
from .permissions import IsPostOwnerOrReadOnly
from .mixins import PostViewMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
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


class ListView(ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = MusicList

class ListDetailView(RetrieveUpdateDestroyAPIView):
    queryset = MusicList.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsPostOwnerOrReadOnly]

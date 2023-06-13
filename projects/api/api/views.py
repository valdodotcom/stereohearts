from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, MusicList
from .serializers import *
from .permissions import IsPostOwnerOrReadOnly
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


class ReviewView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = Review.objects.all().order_by('-created_at')

        if username:
            queryset = queryset.filter(user__username=username)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsPostOwnerOrReadOnly]


class ListView(ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = MusicList.objects.all().order_by('-created_at')

        if username:
            queryset = queryset.filter(user__username=username)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

class ListDetailView(RetrieveUpdateDestroyAPIView):
    queryset = MusicList.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsPostOwnerOrReadOnly]

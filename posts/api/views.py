from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, MusicList
from .serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /posts/',
        'GET /posts/reviews/',
        'GET /posts/reviews/username?=:username',
        'GET /posts/lists/', 
        'GET /posts/lists/username?=:username',
    ]

    return Response(routes) 


class ReviewView(ListCreateAPIView):
    serializer_class = ReviewSerializer

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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ListView(ListCreateAPIView):
    serializer_class = ListSerializer

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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
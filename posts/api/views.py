from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, MusicList, User
from .serializers import *
from rest_framework import status, generics


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


class ReviewView(generics.ListCreateAPIView):
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


class ListView(generics.ListCreateAPIView):
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

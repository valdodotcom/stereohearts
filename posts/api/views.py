from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, MusicList, User
from .serializers import *
from rest_framework import status, generics


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /posts',
        'GET /posts/all', 
        'GET /posts/:username',
        'POST /posts/create-review',
        'POST /posts/create-list'
    ]

    return Response(routes) 


class ReviewView(generics.ListCreateAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class ListView(generics.ListCreateAPIView):
    queryset = MusicList.objects.all().order_by('-created_at')
    serializer_class = ListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

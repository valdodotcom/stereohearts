from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, MusicList, User
from .serializers import *
from rest_framework import status


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


@api_view(['GET'])
def getPosts(request):
    reviews = Review.objects.all().order_by('-created_at')
    music_lists = MusicList.objects.all().order_by('-created_at')

    review_serializer = ReviewSerializer(reviews, many=True)
    music_list_serializer = MusicListSerializer(music_lists, many=True)

    posts = {
        'reviews': review_serializer.data,
        'music_lists': music_list_serializer.data
    }

    return Response(posts)

@api_view(['GET'])
def getUserPosts(request, username):
    user = User.objects.get(username=username)
    reviews = Review.objects.filter(user=user)
    music_lists = MusicList.objects.filter(user=user)

    review_serializer = ReviewSerializer(reviews, many=True)
    music_list_serializer = MusicListSerializer(music_lists, many=True)

    user_posts = {
        'reviews': review_serializer.data,
        'music_lists': music_list_serializer.data
    }

    return Response(user_posts)


@api_view(['POST'])
def createReview(request):
    serializer = CreateReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        review = serializer.save()
        title = serializer.data.get('title')
        return Response({'detail': f"Review '{title}' created successfully."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def createList(request):
    serializer = CreateListSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        music_list = serializer.save()
        title = serializer.data.get('title')
        return Response({'detail': f"List '{title}' created successfully."}, status=status.HTTP_201_CREATED)

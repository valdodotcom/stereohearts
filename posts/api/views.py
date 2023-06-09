from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, MusicList, User
from .serializers import ReviewSerializer, MusicListSerializer

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
    reviews = Review.objects.all()
    music_lists = MusicList.objects.all()

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
    pass

@api_view(['POST'])
def createList(request):
    pass

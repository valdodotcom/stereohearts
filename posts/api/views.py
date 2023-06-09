from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, User
from .serializers import ReviewSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /posts',
        'GET /posts/all', 
        'GET /posts/:username',
        'POST /posts/create',
    ]

    return Response(routes) 


@api_view(['GET'])
def getReviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUserReviews(request, username):
    user = User.objects.get(username=username)
    reviews = Review.objects.filter(user=user)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createReview(request):
    pass
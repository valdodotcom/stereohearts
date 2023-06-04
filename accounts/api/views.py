from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Reviewer, User
from .serializers import ReviewerSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /accounts',
        'GET /accounts/reviewers', 
        'GET /accounts/:username',
        'POST /accounts/register',
        'POST /accounts/login',
        'POST /accounts/logout',
    ]

    return Response(routes) 


@api_view(['GET'])
def getReviewers(request):
    reviewers = Reviewer.objects.all()
    serializer = ReviewerSerializer(reviewers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getReviewer(request, username):
    reviewer = Reviewer.objects.get(user__username=username)
    serializer = ReviewerSerializer(reviewer, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def register(request):
    user_data = request.data.copy()
    password = user_data.get('password')
    hashed_password = make_password(password)
    user_data['password'] = hashed_password

    user_serializer = UserSerializer(data=user_data)
    reviewer_serializer = ReviewerSerializer(data=request.data)

    if user_serializer.is_valid() and reviewer_serializer.is_valid():
        user = user_serializer.save()
        reviewer = reviewer_serializer.save(user=user)

        response_data = {
            'user': user_serializer.data,
            'reviewer': reviewer_serializer.data
        }
        return Response(response_data, status=201)

    errors = {}
    errors.update(user_serializer.errors)
    errors.update(reviewer_serializer.errors)

    return Response(errors, status=400)


@api_view(['POST'])
def loginUser(request):
    username_or_email = request.data.get('username_or_email')
    password = request.data.get('password')

    user = None

    # Check if the username_or_email is an email
    if '@' in username_or_email:
        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            pass

    # If not found by email, check if it's a username
    if user is None:
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or email'}, status=400)

    user = authenticate(request, username=user.username, password=password)

    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response({'detail': 'Logged in successfully!'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=400)


@api_view(['POST'])
def logoutUser(request):
    logout(request)
    return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render, redirect

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
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUser(request, username):
    user = User.objects.get(username=username)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def register(request):
    user_data = request.data.copy()
    password = user_data.get('password')
    hashed_password = make_password(password)
    user_data['password'] = hashed_password

    user_serializer = UserSerializer(data=user_data)

    user_serializer.is_valid(raise_exception=True)  # Validate user_serializer

    user = user_serializer.save()

    response_data = {
        'user': user_serializer.data,
    }
    return Response({'detail': f"User {user_data.get('username')} created successfully."}, status=status.HTTP_201_CREATED)


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
            return Response({'error': 'Invalid username or email'}, status=400)

    # If not found by email, check if it's a username
    if user is None:
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or email'}, status=400)

    user = authenticate(request, username=user.username, password=password)

    if user is not None:
        login(request, user)
        return Response({'detail': 'Logged in successfully!'}, status=status.HTTP_200_OK)
        # response_data = {
        #     'detail': 'Logged in successfully!',
        #     'redirect_url': '/home/'  # Replace with the desired redirect URL
        # }

        # return JsonResponse(response_data, status=200)
    else:
        return Response({'error': 'Invalid username or password'}, status=400)


@api_view(['POST'])
def logoutUser(request):
    logout(request)
    return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)
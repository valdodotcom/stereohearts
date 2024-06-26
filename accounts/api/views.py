from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from os import environ
from dotenv import load_dotenv

load_dotenv()
FRONTEND_URL = environ.get('FRONTEND_URL')


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /accounts/',
        'GET /accounts/users/', 
        'GET /accounts/users/?username=username/',
        'POST /accounts/login/',
        'POST /accounts/logout/',
        'POST /accounts/update/',
        'POST /accounts/destroy/',
    ]

    return Response(routes) 


class ListUsersView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        following = self.request.query_params.get('following', None)

        queryset = User.objects.all().order_by('-date_joined')

        if username:
            queryset = queryset.filter(username=username)

        if following == 'yes':
            user = self.request.user
            queryset = user.following.all()

        return queryset


class GetUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        password = data.get('password')
        hashed_password = make_password(password)
        data['password'] = hashed_password
        user = serializer.save()
        login(self.request, user)


class UpdateUserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        # Get the current user object
        user = self.get_object()

        # Serialize the current user data
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def perform_update(self, serializer):
        data = serializer.validated_data
        password = data.get('password')

        if password:
            hashed_password = make_password(password)
            data['password'] = hashed_password

        serializer.save()
 
    
class DestroyUserView(DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


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
            return Response({'error': 'Invalid username or email.'}, status=400)

    # If not found by email, check if it's a username
    if user is None:
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or email.'}, status=400)

    user = authenticate(request, username=user.username, password=password)

    if user is not None:
        login(request, user)
        response_data = {
            'success': 'Logged in successfully!',
            # 'redirect_url': f'{FRONTEND_URL}/'
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=400)


@api_view(['POST'])
def logoutUser(request):
    logout(request)
    return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class FollowView(viewsets.ViewSet):
    queryset = User.objects

    def follow(self, request, pk):
        own_profile = User.objects.get(username=request.user)
        following_profile = User.objects.get(id=pk)

        # Check if already following
        if following_profile in own_profile.following.all():
            own_profile.following.remove(following_profile)
            return Response({'message': 'Unfollowed'}, status=status.HTTP_200_OK)
        else:
            # Prevent user from following themselves
            if own_profile != following_profile:
                if following_profile in own_profile.blocked_by.all():
                    return Response({'message': 'You cannot follow a user who has blocked you'}, status=status.HTTP_400_BAD_REQUEST)
                if following_profile in own_profile.blocked_users.all():
                    return Response({'message': 'You cannot follow a blocked user'}, status=status.HTTP_400_BAD_REQUEST)
                own_profile.following.add(following_profile)
                return Response({'message': 'Followed'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
            

class BlockView(viewsets.ViewSet):
    queryset = User.objects

    def block(self, request, pk):
        own_profile = User.objects.get(username=request.user)
        blocked_profile = User.objects.get(id=pk)

        # Check if already blocked
        if blocked_profile in own_profile.blocked_users.all():
            own_profile.blocked_users.remove(blocked_profile)
            return Response({'message': 'Unblocked'}, status=status.HTTP_200_OK)
        else:
            # Prevent user from blocking themselves
            if own_profile != blocked_profile:
                own_profile.blocked_users.add(blocked_profile)
                own_profile.following.remove(blocked_profile)
                own_profile.followers.remove(blocked_profile)
                return Response({'message': 'Blocked'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You cannot block yourself'}, status=status.HTTP_400_BAD_REQUEST)
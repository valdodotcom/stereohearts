from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import ListCreateAPIView

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /accounts/',
        'GET /accounts/users/', 
        'GET /accounts/users/username?=:username/',
        'POST /accounts/login/',
        'POST /accounts/logout/',
    ]

    return Response(routes) 


class UserView(ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = User.objects.all().order_by('-date_joined')

        if username:
            queryset = queryset.filter(username=username)
        return queryset

    def perform_create(self, serializer):
        data = serializer.validated_data
        password = data.get('password')
        hashed_password = make_password(password)
        data['password'] = hashed_password
        serializer.save()

        return super().perform_create(serializer)


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
from django.urls import path
from .views import *

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path('', getRoutes),
    path('auth/', obtain_auth_token),

    path('users/', ListUsersView.as_view()),
    path('get-user/<int:pk>/', GetUserView.as_view(), name="get-user"),
    path('register/', CreateUserView.as_view()),
    path('login/', loginUser),
    path('logout/', logoutUser),
    path('update/', UpdateUserView.as_view()),
    path('destroy/', DestroyUserView.as_view())
]
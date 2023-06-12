from django.urls import path
from .views import *

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path('', getRoutes),
    path('auth/', obtain_auth_token),

    path('users/', UserView.as_view()),
    path('login/', loginUser),
    path('logout/', logoutUser),
    path('update/', UpdateUserView.as_view()),
    path('destroy/', DestroyUserView.as_view())
]
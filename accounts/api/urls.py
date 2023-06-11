from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', getRoutes),
    path('users/', UserView.as_view()),
    path('login/', loginUser),
    path('logout/', logoutUser),
    path('update/', UpdateUserView.as_view()),
    path('destroy/', DestroyUserView.as_view())
]
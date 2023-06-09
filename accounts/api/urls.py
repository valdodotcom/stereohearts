from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', getRoutes, name=''),
    path('register/', register, name='register'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('users/', getUsers, name='all'),
    path('<str:username>', getUser, name='user'),
    
]
from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', getRoutes, name=''),
    path('all/', getPosts, name='all'),
    path('<str:username>/', getUserPosts, name='user'),

    path('create-review/', createReview, name='create-review'),
    path('create-list/', createList, name='create-list'),
    
]
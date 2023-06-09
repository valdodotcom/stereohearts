from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', getRoutes, name=''),
    path('all/', getReviews, name='all'),
    path('<str:username>', getUserReviews, name='user'),
    path('create/', createReview, name='create')
]
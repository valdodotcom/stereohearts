from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', getRoutes, name=''),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('reviewers/', getReviewers, name='all'),
    path('<str:username>', getReviewer, name='reviewer'),
    
]
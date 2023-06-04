from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', getRoutes, name=''),
    path('register/', register),
    path('login/', login),
    path('reviewers/', getReviewers),
    path('reviewers/<str:username>', getReviewer),
    
]
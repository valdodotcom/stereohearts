from django.urls import path
from .views import *

urlpatterns = [
    path('', getRoutes),
    path('register/', register),
    path('login/', login),
    path('reviewers/', getReviewers),
    path('reviewers/<str:username>', getReviewer),
    
]
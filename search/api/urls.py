from django.urls import path
from .views import *

app_name = 'search'

urlpatterns = [
    path('lists/', SearchListView.as_view()),
    path('reviews/', SearchReviewView.as_view()),
    path('users/', SearchUserView.as_view()),
    path('projects/', SearchProjectView.as_view()),
    path('artists/', SearchArtistView.as_view()),
    path('all/', SearchAllView.as_view()),
]
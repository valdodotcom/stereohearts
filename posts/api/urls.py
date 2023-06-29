from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', getRoutes, name=''),

    path('reviews/', ReviewView.as_view()),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name="review-detail"),
    path('reviews/<int:pk>/vote', ReviewVoteView.as_view(), name="review-vote"),
    path('reviews/<int:pk>/comment', ReviewCommentView.as_view(), name="review-comment"),
    path('lists/', ListView.as_view()),
    path('lists/<int:pk>/', ListDetailView.as_view(), name="list-detail"),
    path('lists/<int:pk>/vote', ListVoteView.as_view(), name="list-vote"),
    path('lists/<int:pk>/comment', ListCommentView.as_view(), name="list-comment"),
    
]
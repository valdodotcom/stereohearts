from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', getRoutes, name=''),

    path('reviews/', ReviewView.as_view(), name="reviews"),
    path('create-review/', CreateReview.as_view(), name="create-review"),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name="review-detail"),
    path('reviews/<int:pk>/vote', ReviewVoteView.as_view(), name="review-vote"),
    path('reviews/<int:pk>/new-comment', ReviewCommentView.as_view(), name="review-comment"),
    path('reviews/comment/<int:pk>', ReviewCommentVoteView.as_view(), name="review-comment-vote"),

    path('lists/', ListView.as_view()),
    path('add-to-list/', MusicListViewSet.as_view({'post': 'create'}), name="add-to-list"),
    path('lists/<int:pk>/', ListDetailView.as_view(), name="list-detail"),
    path('lists/<int:pk>/vote', ListVoteView.as_view(), name="list-vote"),
    path('lists/<int:pk>/new-comment', ListCommentView.as_view(), name="list-comment"),
    path('lists/comment/<int:pk>', ListCommentVoteView.as_view(), name="list-comment-vote"),
    
]
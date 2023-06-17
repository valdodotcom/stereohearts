from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', getRoutes, name=''),

    path('reviews/', ReviewView.as_view()),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name="review-detail"),
    path('lists/', ListView.as_view()),
    path('lists/<int:pk>/', ListDetailView.as_view(), name="list-detail"),
    
]
from django.urls import path
from .views import *

urlpatterns = [
    path('', getRoutes),
    path('view/', getReviews),
    path('view/<str:username>', getUserReviews),
    path('create/', createReview)
]
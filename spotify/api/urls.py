from django.urls import path
from .views import *

urlpatterns = [
    path('', getRoutes),
    path('auth/', getAuth),
    path('redirect/', getCallback),
    path('is-authenticated', getIsAuthenticated),
    # path('view/<str:username>', getUserReviews),
]
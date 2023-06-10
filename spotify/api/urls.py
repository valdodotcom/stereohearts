from django.urls import path
from .views import *

app_name = 'spotify'

urlpatterns = [
    path('', getRoutes),
    path('auth/', getAuth, name='auth'),
    path('redirect/', getCallback, name='redirect'),
    path('is-authenticated/', getIsAuthenticated, name='is-authenticated'),
    # path('view/<str:username>/', getUserReviews),
]
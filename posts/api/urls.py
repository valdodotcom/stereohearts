from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', getRoutes, name=''),

    path('reviews/', ReviewView.as_view()),
    path('lists/', ListView.as_view()),
    
]
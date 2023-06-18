from django.urls import path
from .views import *

app_name = 'projects'

urlpatterns = [
    path('', getRoutes, name=''),

    path('view-projects/', ProjectView.as_view()),
    path('view-projects/<int:pk>/', ProjectDetailView.as_view(), name="project-detail"),
    path('view-artists/', ArtistView.as_view()),
    path('view-artists/<int:pk>/', ArtistDetailView.as_view(), name="artist-detail"),
    
]
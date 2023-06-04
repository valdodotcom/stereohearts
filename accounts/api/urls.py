from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', getRoutes, name=''),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('reviewers/', getReviewers, name='all'),
    path('<str:username>', getReviewer, name='reviewer'),
    
]
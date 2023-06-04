from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_page, name='register'),
    path('create-reviewer', create_reviewer, name='create-reviewer'),
    path('update-user', update_user, name='update-user'),

    path('', home, name='home')
]
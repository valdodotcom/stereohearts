from django.shortcuts import render, redirect
from accounts.forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.db.models import Q
import requests

from os import environ
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def login_page(request):
    page = 'login'
    STEREOHEARTS_URL = environ.get('STEREOHEARTS_URL')

    if request.method == 'POST':
        response = requests.post('https://api.example.com/endpoint', data={'key': 'value'})
        if response.status_code == 200:
            return redirect('home') 

    context = {'page': page, 'link':STEREOHEARTS_URL}
    return render(request, 'frontend/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
    page = 'register'
    form = UserForm

    context = {'page': page, 'form': form}
    return render(request, 'frontend/login_register.html', context)

def home(request):
    return render(request, 'frontend/home.html')

@login_required(login_url='login')
def update_user(request):
    return render(request, 'frontend/update_user.html')
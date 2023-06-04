from django.shortcuts import render, redirect
from accounts.forms import ReviewerForm, UserForm
from accounts.models import Reviewer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.db.models import Q

# Create your views here.
def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = Reviewer.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid username or password')

    context = {'page': page}
    return render(request, 'frontend/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
    page = 'register'
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('create-reviewer')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'page': page, 'form': form}
    return render(request, 'frontend/login_register.html', context)

@login_required(login_url='login')
def create_reviewer(request):
    page = 'create-reviewer'

    if request.method == 'POST':
        form = ReviewerForm(request.POST)
        if form.is_valid():
            reviewer = form.save(commit=False)
            if reviewer.user != request.user:
                return HttpResponseForbidden("You are not authorized to create a reviewer for this user.")
            reviewer.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    else:
        form = ReviewerForm(initial={'user': request.user})

    context = {'page': page, 'form': form}
    return render(request, 'frontend/create_reviewer.html', context)

def home(request):
    # search
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = Reviewer.objects.filter(
        Q(user__username__icontains=q) |
        Q(display_name__icontains=q)
        )
    
    # topics = Topic.objects.all()
    # room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'users': users}
    return render(request, 'frontend/home.html', context)

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(request, 'frontend/update_user.html', context)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Profile,Project,Ratings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import NewProjectForm,RegisterForm,ProfileUpdateForm,RatingsForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404

from rest_framework.response import Response
from .serializer import ProfileSerializer,ProjectSerializer
from rest_framework.views import APIView

# Create your views here.
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user doesnt exist')

        user = authenticate(request, username= username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'username or password does not exist')

    context = {
        'page':page
    }
    return render(request, 'registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('homepage')

def registerUser(request):
    page = 'register'
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'An error occured during registration')
    context = {
        'form':form,
        'page':page
    }

    return render(request, 'registration/login.html', context)

def homepage(request):
    """Default landing page"""
    projects = Project.objects.all()
    return render(request,'home.html',{'projects':projects})

@login_required(login_url='login')
def rate_project(request, id):
    current_user = request.user
    try:
        project = Project.objects.get(id = id)
    except ObjectDoesNotExist:
        raise Http404()
    ratings = project.ratings_set.all()

    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.rater = current_user
            rating.project = project
            rating.save()
            return redirect('homepage')
    else:
        form = RatingsForm()   
    
    return render(request, 'rate_project.html', {'project':project, 'form':form , 'ratings':ratings})
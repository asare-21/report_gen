from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import UserModel, FMModel, TVModel
from django.contrib.auth.models import User
from django.http import Http404
from django.template import RequestContext
import unames
import requests
from asgiref.sync import sync_to_async

LOGIN_URL = 'login/'
REDIRECT_FIELD_NAME = 'login'


# Create your views here.
@login_required(login_url=LOGIN_URL, redirect_field_name=REDIRECT_FIELD_NAME)
def index(request):
    # pass current user to template
    completed = FMModel.objects.filter(completed=True).count(
    ) + TVModel.objects.filter(completed=True).count()
    pending = FMModel.objects.filter(completed=False).count(
    ) + TVModel.objects.filter(completed=False).count()
    print(completed, pending)
    data = {'user': request.user, 'completed': completed, 'pending': pending}
    return render(request, 'ease/index.html', data)


def login_(request):
    # redirect if user is logged in
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == 'POST':
        # a user is logging in
        # get username and password
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate user
        user = authenticate(request, username=username, password=password)
        # if user is valid, login
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, 'ease/login.html', {'error': 'Invalid username or password'})
    return render(request, 'ease/login.html')


def logout_(request):
    # logout a user here
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    try:    
        if request.method == 'POST':
            # a user is creating an account
            # create a new user
            first_name = request.POST.get('first_name').strip()
            last_name = request.POST.get('last_name').strip()
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('repeat_password')
            phone = request.POST.get('phone')
            first_name_list = first_name.split()
            last_name_list = last_name.split()
            username = request.POST.get('username')
            existing_user = User.objects.filter(email=email).exists()
            existing_username = User.objects.filter(username=username).exists()
            if(existing_username):
                return render(request, 'ease/register.html', {'error': 'An account with this username address already exists'})
            if(existing_user):
                return render(request, 'ease/register.html', {'error': 'An account with this email address already exists'})
            # check passwords
            if password != password_confirm:
                return render(request, 'ease/register.html', {'error': 'Passwords do not match'})
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, password=password, username=username.lower())
            # save user
            user.save()
            # create NSP Model and Link to user
            nsp = UserModel(user=user, nsp=True)
            nsp.save()
            # send login details to user
            user = {'username': username, 'password': password, 'email': email, 'phone': phone}
          
            return redirect('login')
        return render(request, 'ease/register.html')
    except Exception as e:
        print(e)
        return render(request, 'ease/register.html', {'error': 'Something went wrong'})

def notFound(request, exception):
    response = render(
        'ease/404.html',
        context_instance=RequestContext(request)
    )
    response.status_code = 404
    return response


def error403(request, exception):
    response = render(
        'ease/403.html',
        context_instance=RequestContext(request)
    )
    response.status_code = 403
    return response


def error500(request):
    response = render(
        request,
        'ease/500.html',

    )
    response.status_code = 500
    return response


@login_required(login_url=LOGIN_URL, redirect_field_name=REDIRECT_FIELD_NAME)
def fm_general(request):
    # fetch all fm models
    fm_models = FMModel.objects.all()
    if request.method == 'POST':
        # a user is creating an account
        # create a new user
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if completed == 'on':
            completed = True
        else:
            completed = False
        # create NSP Model and Link to user
        fm_model = FMModel(title=title, description=description, completed=completed)
        fm_model.save()
        return redirect('fm_general')
    return render(request, 'ease/fm.html', {'fm_models': fm_models,'user': request.user})


@login_required(login_url=LOGIN_URL, redirect_field_name=REDIRECT_FIELD_NAME)
def fm_single(request, id):
    try:
        fm = FMModel.objects.get(id=id)
        return render(request, 'ease/fm_single.html', {'fm': fm})
    except Exception as e:
        return render(request, 'ease/fm_single.html',{'error': 'Something went wrong'})


@login_required(login_url=LOGIN_URL, redirect_field_name=REDIRECT_FIELD_NAME)
def tv_general(request):
    return render(request, 'ease/tv_general.html')


@login_required(login_url=LOGIN_URL, redirect_field_name=REDIRECT_FIELD_NAME)
def tv_single(request, id):
    return render(request, 'ease/tv_single.html')

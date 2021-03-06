from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from ease.helpers import docxToPdf
from .models import UserModel, FMModel, TVModel, NotificationModel
from django.contrib.auth.models import User
from django.http import Http404
from django.template import RequestContext
import unames
import requests
import asyncio
from asgiref.sync import sync_to_async
from django.core import serializers


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
    notification_count = NotificationModel.objects.filter(
        user=request.user, seen=False).count()
    notifications = NotificationModel.objects.filter(
        user=request.user, seen=False).order_by('created_at')
    pending_fm = FMModel.objects.filter(completed=False)
    pending_tv = TVModel.objects.filter(completed=False)
    # spread operator inserts the content of the lists
    pending_reports = [*pending_fm, *pending_tv]
    data = {'user': request.user, 'completed': completed, 'pending': pending,
            'notification_count': notification_count, 'notifications': notifications, 'pending_reports': pending_reports}
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
            user = {'username': username, 'password': password,
                    'email': email, 'phone': phone}

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
    try:
        fm_models = FMModel.objects.all().order_by('created_at')
        fm_models_serialized = serializers.serialize("json", fm_models)
        notification_count = NotificationModel.objects.filter(
            user=request.user, seen=False).count()
        notifications = NotificationModel.objects.filter(
            user=request.user, seen=False).order_by('created_at')
        if request.method == 'POST':
            # a user is creating an account
            # create a new user
            station_officer = request.POST.get('station_officer')
            station_name = request.POST.get('station_name')
            staff_stength = request.POST.get('staff_strength')
            security_post = request.POST.get('security_post')
            security_post_comment = request.POST.get('security_post_comment')
            signpost = request.POST.get('signpost')
            signpost_comment = request.POST.get('signpost_comment')
            epa = request.POST.get('epa')
            epa_comment = request.POST.get('epa_comment')
            fire = request.POST.get('fire')
            fire_comment = request.POST.get('fire_comment')
            earthed_mast = request.POST.get('earthed_mast')
            earthed_mast_comment = request.POST.get('earthed_mast_comment')
            mast_color = request.POST.get('mast_color')
            mast_color_comment = request.POST.get('mast_color_comment')
            directional_antenna = request.POST.get('directional_antenna')
            directional_antenna_comment = request.POST.get(
                'directional_antenna_comment')
            cavity = request.POST.get('cavity')
            cavity_comment = request.POST.get('cavity_comment')
            backup = request.POST.get('backup')
            backup_comment = request.POST.get('backup_comment')
            equipment_list = request.POST.get('equipment_list')
            equipment_list_comment = request.POST.get('equipment_list_comment')
            on_air = request.POST.get('on_air')
            on_air_comment = request.POST.get('on_air_comment')
            studio_ventilated = request.POST.get('studio_ventilated')
            studio_ventilated_comment = request.POST.get(
                'studio_ventilated_comment')
            acoustic_panels = request.POST.get('acoustic_panels')
            acoustic_panels_comment = request.POST.get(
                'acoustic_panels_comment')
            secure_studio = request.POST.get('secure_studio')
            secure_studio_comment = request.POST.get('secure_studio_comment')
            reception = request.POST.get('reception')
            reception_comment = request.POST.get('reception_comment')
            mast_height = 0 if request.POST.get(
                'mast_height') == "" else int(request.POST.get('mast_height'))
            antenna_gain = 0 if request.POST.get(
                'antenna_gain') == "" else int(request.POST.get('gain'))
            make_model_antenna = request.POST.get('make_model')
            frequency = 0 if request.POST.get(
                'frequency') == "" else int(request.POST.get('frequency'))
            physical_location = request.POST.get('physical_location')
            station_coords = request.POST.get('station_coords')
            comments = request.POST.get('comments')
            # create FM model
            fm_model = FMModel(created_by=request.user, comments_remarks=comments, coords=station_coords,
                               physical_location=physical_location, operating_frequency=frequency, make_and_model_antenna=make_model_antenna, antenna_gain=antenna_gain, mast_height=mast_height, reception_comment=reception_comment, reception=reception, secure_door_comment=secure_studio_comment, secure_door=secure_studio, acoustic_panel=acoustic_panels, acoustic_panel_comment=acoustic_panels_comment, ventillation_equipment=studio_ventilated, ventillation_equipment_comment=studio_ventilated_comment, on_air_lighting=on_air, on_air_lighting_comment=on_air_comment, equipment_sheet=equipment_list, equipment_sheet_comment=equipment_list_comment, backup_power=backup, backup_power_comment=backup_comment, cavity_filter=cavity, cavity_filter_comment=cavity_comment, directional_antenna=directional_antenna, directional_antenna_comment=directional_antenna_comment, mast_right_colors=mast_color, mast_right_colors_comment=mast_color_comment, mast_earthed=earthed_mast, mast_earthed_comment=earthed_mast_comment, name_of_station=station_name, station_officer=station_officer, staff_strength=staff_stength, security_post=security_post, security_post_comment=security_post_comment,   epa_permit=epa, epa_permit_comment=epa_comment, signage_board=signpost, signage_board_comment=signpost_comment)
            fm_model.save()
            return redirect('fm_general')
        return render(request, 'ease/fm.html', {'fm_models': fm_models, 'user': request.user, 'fm_models_serialize': fm_models_serialized, 'notification_count': notification_count, 'notifications': notifications})
    except Exception as e:
        print(e)
        return render(request, 'ease/fm.html', {'error': "Something went wrong"})


@login_required(login_url=LOGIN_URL, redirect_field_name=REDIRECT_FIELD_NAME)
def fm_single(request, id):
    try:
        fm = FMModel.objects.get(id=id)
        return render(request, 'ease/fm_single.html', {'fm': fm})
    except Exception as e:
        return render(request, 'ease/fm_single.html', {'error': 'Something went wrong'})


@login_required(login_url=LOGIN_URL, redirect_field_name=REDIRECT_FIELD_NAME)
def tv_general(request):
    notification_count = NotificationModel.objects.filter(
        user=request.user, seen=False).count()
    notifications = NotificationModel.objects.filter(
        user=request.user, seen=False).order_by('created_at')
    return render(request, 'ease/tv.html', {'user': request.user, 'notification_count': notification_count, 'notifications': notifications})


@login_required(login_url=LOGIN_URL, redirect_field_name=REDIRECT_FIELD_NAME)
def tv_single(request, id):
    return render(request, 'ease/tv_single.html')

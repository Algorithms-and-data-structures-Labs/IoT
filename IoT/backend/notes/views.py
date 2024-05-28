import token
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Telemetry, Devices
from django.forms.models import model_to_dict
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User 
from django.db.models import Q
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.db import transaction
from django import forms
from django.core.exceptions import ValidationError
from .models import Devices
from .models import DeviceType
from .forms import DeviceForm
import uuid
from uuid import uuid4
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@api_view(['GET', 'POST'])
def telemetry(request):
    token = request.query_params['token']

    if request.method == 'GET':
        print("GET", request.data)
        #if request.is_authenticated:
        if True:
            try:
                try:
                    count = int(request.query_params['count'])
                except:
                    count = 1

                telemetry = Telemetry.objects.filter(token=token).order_by('-ressived_time')[:count].values()
                return Response(telemetry[::-1], status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'POST':
        print("POST", request.data)
        #if request.is_authenticated:
        if True:
            try:
                Devices.objects.get(token=token)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            telemetry = Telemetry.objects.create(
                token=token,
                data=request.data
            )
            return Response(model_to_dict(telemetry), status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_418_IM_A_TEAPOT)

@api_view(['GET',])
def type(request):
    token = request.query_params['token']

    if request.method == 'GET':
        print("GET", request.data)
        #if request.is_authenticated:
        if True:
            try:
                device = Devices.objects.get(token=token)
                return Response(device.type.type, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_418_IM_A_TEAPOT)

def index(request):
    return render(request, 'index.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('list_devices')
        else:
            return render(request, 'login.html', {'error_message': 'Неверное имя пользователя или пароль'})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                login(request, user)
                messages.success(request, 'Регистрация прошла успешно. Добро пожаловать!')
                return redirect('register')
            except IntegrityError:
                messages.error(request, 'Пользователь с таким именем уже существует.')
        else:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'register.html', {'error_message': 'Пароли не совпадают'})
    return render(request, 'register.html')


def register_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            if request.user.is_authenticated:
                device.owner = request.user.id
                device.token = uuid.uuid4().hex
                try:
                    device.save()
                    messages.success(request, 'Устройство успешно зарегистрировано.')
                    return redirect('list_devices')
                except IntegrityError:
                    messages.error(request, 'Устройство с таким модельным номером или серийным номером уже существует.')
                    return render(request, 'register_device.html', {'form': form, 'devices': Devices.objects.filter(owner=request.user.id)})
            else:
                messages.error(request, 'Пожалуйста, войдите в систему перед регистрацией устройства.')
                return redirect('login')
        else:
            messages.error(request, 'Устройство с таким модельным номером или серийным номером уже существует!')
    else:
        form = DeviceForm()
    return render(request, 'register_device.html', {'form': form})

def list_devices(request):
    if not request.user.is_authenticated:
        return redirect('login')

    devices = Devices.objects.filter(owner=request.user.id)
    return render(request, 'list_devices.html', {'devices': devices})


def delete_device(request):
    data = json.loads(request.body)
    device_id = data.get('device_id')
    try:
        device = Devices.objects.get(id=device_id, owner=request.user.id)  
        device.delete()
        return JsonResponse({'status': 'success'}, status=200)
    except Devices.DoesNotExist:  
        return JsonResponse({'status': 'not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



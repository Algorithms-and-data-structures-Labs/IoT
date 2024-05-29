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


def list_devices(request):
    devices = Devices.objects.all()
    return render(request, 'list_devices.html', {'devices': devices})


def delete_device(request):
    data = json.loads(request.body)
    device_id = data.get('device_id')
    try:
        device = Devices.objects.get(id=device_id)
        device.delete()
        return JsonResponse({'status': 'success'}, status=200)
    except Devices.DoesNotExist:  
        return JsonResponse({'status': 'not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



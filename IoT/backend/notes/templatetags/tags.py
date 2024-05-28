from django import template
from notes.models import *
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

def get_lastest_telemetry(token):
    try:
        return Telemetry.objects.filter(token=token).latest('ressived_time').data
    except ObjectDoesNotExist:
        return "-"
    
get_lastest_telemetry = register.simple_tag(get_lastest_telemetry)
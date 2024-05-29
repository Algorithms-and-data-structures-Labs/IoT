from datetime import datetime
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
class Telemetry(models.Model):
    token = models.CharField(max_length=128)
    ressived_time = models.DateTimeField(default=timezone.now)
    data = models.JSONField()

class DeviceType(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        db_table = 'device_types'

    def __str__(self):
        return self.type

class Devices(models.Model):
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, blank=True, null=True)  

    def __str__(self):
        return f"{self.model} ({self.serial_number}) - Token: {self.token}"
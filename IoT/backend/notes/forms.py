from django import forms
from .models import Devices, DeviceType

class DeviceForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=DeviceType.objects.all(), empty_label="Выберите тип")

    class Meta:
        model = Devices
        fields = ['model', 'serial_number', 'type', 'owner', 'token']

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
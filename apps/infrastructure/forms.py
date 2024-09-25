from django import forms

from .models import Location, IotCategories, IotDevices


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["location"]


class IotCategoriesForm(forms.ModelForm):
    class Meta:
        model = IotCategories
        fields = ['categoryName']


class IotDevicesForm(forms.ModelForm):
    class Meta:
        model = IotDevices
        fields = ["deviceId", "deviceName", "deviceLabel", "deviceCategory", "location"]

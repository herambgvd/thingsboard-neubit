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

    def __init__(self, *args, **kwargs):
        # Accept `team` parameter
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)

        # Customize the queryset for selectBranch
        if team:
            self.fields['location'].queryset = Location.objects.filter(team=team)

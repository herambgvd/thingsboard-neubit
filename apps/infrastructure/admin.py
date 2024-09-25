from django.contrib import admin

from .models import Location, IotCategories, IotDevices, ThermostatSensor

# Register your models here.

admin.site.register(Location)
admin.site.register(IotCategories)
admin.site.register(IotDevices)
admin.site.register(ThermostatSensor)

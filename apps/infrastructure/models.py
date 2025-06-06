import uuid

from django.db import models

from apps.teams.models import BaseTeamModel


# Create your models here.

class Location(BaseTeamModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    location = models.CharField(max_length=35)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.location

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class IotCategories(BaseTeamModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

    class Meta:
        verbose_name = "IOT Category"
        verbose_name_plural = "IOT Categories"


class IotDevices(BaseTeamModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    deviceId = models.CharField(max_length=100)
    deviceName = models.CharField(max_length=100)
    deviceLabel = models.CharField(max_length=100, blank=True, null=True)
    deviceCategory = models.ForeignKey(IotCategories, on_delete=models.CASCADE, related_name="iot_device")
    deviceResponse = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE,
                                 related_name='location_device')
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.deviceName

    class Meta:
        verbose_name = "IOT Device"
        verbose_name_plural = "IOT Devices"


######## Iot Thermostat Section ######
class ThermostatSensor(BaseTeamModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    thermostate_device = models.ForeignKey(IotDevices, on_delete=models.CASCADE, related_name="thermostat_sensor_data")
    pm_ten = models.CharField(max_length=100, null=True, blank=True)  # Done
    pm_two_five = models.CharField(max_length=100, null=True, blank=True)  # Done
    noise = models.CharField(max_length=100, null=True, blank=True)  # Done
    co_two = models.CharField(max_length=100, null=True, blank=True)  # Done
    firmware_version = models.CharField(max_length=100, null=True, blank=True)
    fs = models.CharField(max_length=100, null=True, blank=True)
    mac = models.CharField(max_length=100, null=True, blank=True)
    hum = models.CharField(max_length=100, null=True, blank=True)  # Done
    voc = models.CharField(max_length=100, null=True, blank=True)  # Done
    state = models.CharField(max_length=100, null=True, blank=True)
    lux = models.CharField(max_length=100, null=True, blank=True)  # Done
    cv = models.CharField(max_length=100, null=True, blank=True)
    hv = models.CharField(max_length=100, null=True, blank=True)
    t_sen = models.CharField(max_length=100, null=True, blank=True)
    s_temp = models.CharField(max_length=100, null=True, blank=True)
    c_h = models.CharField(max_length=100, null=True, blank=True)
    occ = models.CharField(max_length=100, null=True, blank=True)
    site_id = models.CharField(max_length=100, null=True, blank=True)
    room_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.thermostate_device.deviceName} -- {self.created_at}"

    class Meta:
        verbose_name = "Thermostat Sensor"
        verbose_name_plural = "Thermostat Sensors"

import datetime

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.infrastructure.models import IotDevices, IotCategories
from apps.teams.models import Team
from .models import IotConfig


@receiver(post_save, sender=IotConfig)
def get_devices(sender, instance, created, **kwargs):
    """
    Make request to API, get all devices, segregate data into Devices and Categories,
    and save the token and refresh token in the instance.
    """

    if created:
        username = instance.username
        password = instance.password
        login_url = f'{settings.THINGSBOARD_BASE_URL}/auth/login'
        login_body = {
            "username": username,
            "password": password
        }

        try:
            # Request to get the token
            response = requests.post(login_url, json=login_body)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            token = data["token"]
            refresh_token = data.get("refreshToken")  # Get refresh token if available

            # Save the tokens in the instance
            instance.token = token
            instance.refresh_token = refresh_token
            instance.save()

            bearer_token = "Bearer " + token
            devices_url = f'{settings.THINGSBOARD_BASE_URL}/user/devices'
            pageParams = {
                "pageSize": 100,
                "page": 0
            }

            # Request to get devices
            devices_response = requests.get(devices_url, params=pageParams, headers={"x-authorization": bearer_token})
            devices_response.raise_for_status()  # Check for HTTP errors
            devices = devices_response.json()["data"]

            # Create or get categories and devices
            for cate in devices:
                category = cate['type']
                IotCategories.objects.get_or_create(categoryName=category, team=Team.objects.get(id=instance.team.id))

            for device in devices:
                categorySelect = device['type']
                IotDevices.objects.get_or_create(
                    deviceId=device['id']['id'],
                    deviceName=device['name'],
                    deviceLabel=device.get('label', ''),
                    deviceCategory=IotCategories.objects.get(categoryName=categorySelect,
                                                             team=Team.objects.get(id=instance.team.id)),
                    created_at=datetime.datetime.fromtimestamp(device['createdTime'] // 1e3),
                    team=Team.objects.get(id=instance.team.id)
                )
                print(f"Device Created: {device['name']}")

        except requests.RequestException as e:
            # Handle any request-related errors
            print(f"Error fetching devices: {e}")
        except KeyError as e:
            # Handle any JSON decoding or missing key errors
            print(f"Error in response data: {e}")

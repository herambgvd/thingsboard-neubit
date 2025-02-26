import datetime
import requests
from celery import shared_task
from apps.settings.models import IotConfig
from .models import IotDevices, ThermostatSensor, IotCategories

# Define the ThingsBoard login URL and the telemetry URL
THINGSBOARD_LOGIN_URL = "https://thingsboard.cloud/api/auth/login"
TELEMETRY_URL = "https://thingsboard.cloud/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries"


@shared_task
def thermostat_sensor_task():
    current_datetime = str(datetime.date.today())

    # Fetch all IoT configurations with username and password
    iot_configs = IotConfig.objects.all()

    for config in iot_configs:
        # Step 1: Authenticate and get the token
        login_response = requests.post(
            THINGSBOARD_LOGIN_URL,
            json={
                "username": config.username,
                "password": config.password
            }
        )

        if login_response.status_code == 200:
            token = login_response.json().get("token")
            headers = {
                "Content-Type": "application/json",
                "X-Authorization": f"Bearer {token}"
            }

            # Step 2: Fetch the category 'IEQ thermostat' from IotCategories
            try:
                thermostat_category = IotCategories.objects.get(categoryName="IEQ thermostat", team=config.team)
            except IotCategories.DoesNotExist:
                print("IEQ thermostat category does not exist.")
                continue

            # Step 3: Fetch all IoT Devices where deviceCategory is 'IEQ thermostat' and team matches
            thermostat_devices = IotDevices.objects.filter(deviceCategory=thermostat_category, team=config.team)

            for device in thermostat_devices:
                # Step 4: Fetch telemetry data for each device
                telemetry_response = requests.get(
                    TELEMETRY_URL.format(device_id=device.deviceId),
                    headers=headers
                )

                if telemetry_response.status_code == 200:
                    telemetry_data = telemetry_response.json()

                    # Step 5: Parse telemetry data and create a new ThermostatSensor object
                    ThermostatSensor.objects.create(
                        thermostate_device=device,
                        pm_ten=telemetry_data.get("PM10", [{}])[0].get("value"),
                        pm_two_five=telemetry_data.get("PM2.5", [{}])[0].get("value"),
                        noise=telemetry_data.get("Noise", [{}])[0].get("value"),
                        co_two=telemetry_data.get("CO2", [{}])[0].get("value"),
                        firmware_version=telemetry_data.get("firmware_version", [{}])[0].get("value"),
                        fs=telemetry_data.get("FS", [{}])[0].get("value"),
                        mac=telemetry_data.get("MAC", [{}])[0].get("value"),
                        hum=telemetry_data.get("HUM", [{}])[0].get("value"),
                        voc=telemetry_data.get("VOC", [{}])[0].get("value"),
                        state=telemetry_data.get("STATE", [{}])[0].get("value"),
                        lux=telemetry_data.get("Lux", [{}])[0].get("value"),
                        cv=telemetry_data.get("CV", [{}])[0].get("value"),
                        hv=telemetry_data.get("HV", [{}])[0].get("value"),
                        t_sen=telemetry_data.get("T_Sen", [{}])[0].get("value"),
                        s_temp=telemetry_data.get("S_Temp", [{}])[0].get("value"),
                        c_h=telemetry_data.get("C_H", [{}])[0].get("value"),
                        occ=telemetry_data.get("OCC", [{}])[0].get("value"),
                        site_id=telemetry_data.get("site_id", [{}])[0].get("value"),
                        room_number=telemetry_data.get("room_number", [{}])[0].get("value"),
                        team=config.team  # Associate the team from IotConfig
                    )
                else:
                    print(f"Failed to fetch telemetry data for device {device.deviceName}")
        else:
            print(f"Failed to login for config: {config.id}")

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from health_check.views import MainView
from django.utils.timezone import now

from apps.infrastructure.models import IotDevices, IotCategories, Location, ThermostatSensor
from apps.settings.models import TeamProfileImage
from apps.teams.decorators import login_and_team_required


def home(request):
    if request.user.is_authenticated:
        team = request.team
        if team:
            return HttpResponseRedirect(reverse("web_team:home", args=[team.slug]))
        else:
            messages.info(
                request,
                _(
                    "You are not a part of team please contact your administrator."
                ),
            )
            return HttpResponseRedirect(reverse("teams:manage_teams"))
    else:
        return render(request, "web/landing_page.html")


@login_and_team_required(login_url="account_login")
def team_home(request, team_slug):
    assert request.team.slug == team_slug

    try:
        category = IotCategories.objects.get(categoryName="IEQ thermostat", team=request.team)
    except IotCategories.DoesNotExist:
        category = None

    locations_with_devices = []

    if category:
        today = now().date()

        locations = Location.objects.filter(team=request.team)

        for location in locations:
            devices = IotDevices.objects.filter(
                team=request.team,
                deviceCategory=category,
                location=location
            )

            device_data = []

            for device in devices:
                # Latest reading
                latest_sensor = device.thermostat_sensor_data.order_by("-created_at").first()

                # Today's average values
                today_sensors = device.thermostat_sensor_data.filter(
                    created_at__date=today
                ).exclude(pm_ten__isnull=True, pm_two_five__isnull=True)

                def to_float(val):
                    try:
                        return float(val)
                    except (TypeError, ValueError):
                        return 0.0

                pm_ten_avg = 0.0
                pm_two_five_avg = 0.0

                if today_sensors.exists():
                    pm_ten_avg = sum([to_float(s.pm_ten) for s in today_sensors]) / today_sensors.count()
                    pm_two_five_avg = sum([to_float(s.pm_two_five) for s in today_sensors]) / today_sensors.count()

                device_data.append({
                    "device": device,
                    "latest_sensor": latest_sensor,
                    "pm_ten_avg": round(pm_ten_avg, 2),
                    "pm_two_five_avg": round(pm_two_five_avg, 2),
                })

            if device_data:
                locations_with_devices.append({
                    "location": location,
                    "devices": device_data
                })

    profile_image = TeamProfileImage.objects.get(team=request.team)

    return render(
        request,
        "teams/teams_dashboard.html",
        context={
            "team": request.team,
            "active_tab": "dashboard",
            "page_title": _("{team} Dashboard").format(team=request.team),
            "locations_with_devices": locations_with_devices,
            "profile_image": profile_image
        },
    )


def simulate_error(request):
    raise Exception("This is a simulated error.")


class HealthCheck(MainView):
    def get(self, request, *args, **kwargs):
        tokens = settings.HEALTH_CHECK_TOKENS
        if tokens and request.GET.get("token") not in tokens:
            raise Http404
        return super().get(request, *args, **kwargs)

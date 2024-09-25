from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from health_check.views import MainView

from apps.infrastructure.models import IotDevices, IotCategories
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
    # Ensure that the requested team matches the slug in the URL
    assert request.team.slug == team_slug

    # Fetch all devices under the specified category and team
    thermostat_device = IotDevices.objects.filter(
        team=request.team,
        deviceCategory=IotCategories.objects.get(categoryName="IEQ thermostat")
    ).all()

    # Fetch the latest thermostat data for each device
    thermostat_device_sensor_data = {
        device.id: device.thermostat_sensor_data.order_by('-created_at').first()
        for device in thermostat_device
    }

    return render(
        request,
        "teams/teams_dashboard.html",
        context={
            "team": request.team,
            "active_tab": "dashboard",
            "page_title": _("{team} Dashboard").format(team=request.team),
            "thermostat_device": thermostat_device,
            "thermostat_device_sensor_data": thermostat_device_sensor_data,
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

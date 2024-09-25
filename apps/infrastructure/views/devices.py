from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.infrastructure.forms import IotDevicesForm
from apps.infrastructure.models import IotDevices
from apps.teams.decorators import login_and_team_required


# Branch Views
@login_and_team_required(login_url='account_login')
def device(request, team_slug):
    deviceAll = IotDevices.objects.filter(team=request.team).order_by('-created_at')
    context = {'deviceAll': deviceAll}
    return render(request, 'infrastructure/devices/main.html', context)


@login_and_team_required(login_url='account_login')
def device_create(request, team_slug):
    if request.method == 'POST':
        form = IotDevicesForm(request.POST)
        if form.is_valid():
            # Ensure the form is saved before proceeding
            data = form.save(commit=False)
            data.team = request.team
            data.save()
            messages.success(request, "Device Created Successfully")
            return redirect('Infrastructure:device_home', team_slug=team_slug)
    else:
        form = IotDevicesForm()
    context = {'form': form}
    return render(request, 'infrastructure/devices/device_create.html', context)


@login_and_team_required(login_url='account_login')
def device_update(request, team_slug, deviceId):
    device_instance = get_object_or_404(IotDevices, pk=deviceId)
    if request.method == 'POST':
        form = IotDevicesForm(request.POST, instance=device_instance)
        if form.is_valid():
            # Ensure the form is saved before proceeding
            data = form.save(commit=False)
            data.team = request.team
            data.save()
            messages.success(request, "Device Updated Successfully.")
            return redirect('Infrastructure:device_home', team_slug=team_slug)
    else:
        form = IotDevicesForm(instance=device_instance)
    context = {'form': form, 'device_instance': device_instance}
    return render(request, 'infrastructure/devices/device_update.html', context)


@login_and_team_required(login_url='account_login')
def device_delete(request, team_slug, deviceId):
    device_instance = get_object_or_404(IotDevices, pk=deviceId)
    if request.method == 'POST':
        # Delete the database record
        device_instance.delete()
        messages.success(request, "Device Deleted Successfully")
        return redirect('Infrastructure:device_home', team_slug=team_slug)
    context = {'object': device_instance}
    return render(request, 'infrastructure/devices/device_delete_conf.html', context)

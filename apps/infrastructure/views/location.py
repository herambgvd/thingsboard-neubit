from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.infrastructure.forms import LocationForm
from apps.infrastructure.models import Location
from apps.teams.decorators import login_and_team_required


# Branch Views
@login_and_team_required(login_url='account_login')
def location(request, team_slug):
    locationAll = Location.objects.filter(team=request.team).order_by('-created_at')
    context = {'locationAll': locationAll}
    return render(request, 'infrastructure/location/main.html', context)


@login_and_team_required(login_url='account_login')
def location_create(request, team_slug):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            # Ensure the form is saved before proceeding
            data = form.save(commit=False)
            data.team = request.team
            data.save()
            return redirect('Infrastructure:location_home', team_slug=team_slug)
    else:
        form = LocationForm()
    context = {'form': form}
    return render(request, 'infrastructure/location/location_create.html', context)


@login_and_team_required(login_url='account_login')
def location_update(request, team_slug, locationId):
    location_instance = get_object_or_404(Location, pk=locationId)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location_instance)
        if form.is_valid():
            # Ensure the form is saved before proceeding
            data = form.save(commit=False)
            data.team = request.team
            data.save()
            return redirect('Infrastructure:location_home', team_slug=team_slug)
    else:
        form = LocationForm(instance=location_instance)
    context = {'form': form, 'location_instance': location_instance}
    return render(request, 'infrastructure/location/location_update.html', context)


@login_and_team_required(login_url='account_login')
def location_delete(request, team_slug, locationId):
    location_instance = get_object_or_404(Location, pk=locationId)
    if request.method == 'POST':
        # Delete the database record
        location_instance.delete()
        messages.success(request, "Location Deleted Successfully")
        return redirect('Infrastructure:location_home', team_slug=team_slug)
    context = {'object': location_instance}
    return render(request, 'infrastructure/location/location_delete_conf.html', context)

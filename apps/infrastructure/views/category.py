from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from apps.infrastructure.forms import IotCategoriesForm
from apps.infrastructure.models import IotCategories
from apps.teams.decorators import login_and_team_required


# Branch Views
@login_and_team_required(login_url='account_login')
def category(request, team_slug):
    categoryAll = IotCategories.objects.filter(team=request.team).order_by('-created_at')
    context = {'categoryAll': categoryAll}
    return render(request, 'infrastructure/category/main.html', context)


@login_and_team_required(login_url='account_login')
def category_create(request, team_slug):
    if request.method == 'POST':
        form = IotCategoriesForm(request.POST)
        if form.is_valid():
            # Ensure the form is saved before proceeding
            data = form.save(commit=False)
            data.team = request.team
            data.save()
            messages.success(request, "Category Created Successfully")
            return redirect('Infrastructure:category_home', team_slug=team_slug)
    else:
        form = IotCategoriesForm()
    context = {'form': form}
    return render(request, 'infrastructure/category/category_create.html', context)


@login_and_team_required(login_url='account_login')
def category_update(request, team_slug, categoryId):
    category_instance = get_object_or_404(IotCategories, pk=categoryId)
    if request.method == 'POST':
        form = IotCategoriesForm(request.POST, instance=category_instance)
        if form.is_valid():
            # Ensure the form is saved before proceeding
            data = form.save(commit=False)
            data.team = request.team
            data.save()
            print("Category Updated Successfully")
            return redirect('Infrastructure:category_home', team_slug=team_slug)
    else:
        form = IotCategoriesForm(instance=category_instance)
    context = {'form': form, 'category_instance': category_instance}
    return render(request, 'infrastructure/category/category_update.html', context)


@login_and_team_required(login_url='account_login')
def category_delete(request, team_slug, categoryId):
    category_instance = get_object_or_404(IotCategories, pk=categoryId)
    if request.method == 'POST':
        # Delete the database record
        category_instance.delete()
        messages.success(request, "Category Deleted Successfully")
        return redirect('Infrastructure:category_home', team_slug=team_slug)
    context = {'object': category_instance}
    return render(request, 'infrastructure/category/category_delete_conf.html', context)

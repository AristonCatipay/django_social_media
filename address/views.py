from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegionForm, ProvinceForm, CityMunicipalityForm, BarangayForm
from .models import Region, Province, City_Municipality, Barangay

@login_required
def create_region(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successful! Region has been saved.')
    else:
        form = RegionForm()
    
    return render(request, 'address/form.html', {
        'title': 'Create New Region',
        'form': form,
    })

@login_required
def update_region(request, primary_key):
    region = get_object_or_404(Region, id = primary_key)

    if request.method == 'POST':
        form = RegionForm(request.POST, instance=region)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successful! Region has been updated.')
    else: 
        form = RegionForm(instance=region)

    return render(request, 'address/form.html', {
        'title': 'Edit Region',
        'form': form,
    })

@login_required
def create_province(request):
    if request.method == 'POST':
        form = ProvinceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successful! Province has been saved.')
    else:
        form = ProvinceForm()
    
    return render(request, 'address/form.html', {
        'title': 'Create New Province',
        'form': form,
    })
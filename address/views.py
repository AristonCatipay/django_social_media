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

@login_required
def update_province(request, primary_key):
    province = get_object_or_404(Province, id = primary_key)

    if request.method == 'POST':
        form = ProvinceForm(request.POST, instance=province)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successful! Province has been updated.')
    else: 
        form = ProvinceForm(instance=province)

    return render(request, 'address/form.html', {
        'title': 'Edit Province',
        'form': form,
    })

@login_required
def create_city_municipality(request):
    if request.method == 'POST':
        form = CityMunicipalityForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successful! City Municipality has been saved.')
    else:
        form = CityMunicipalityForm()
    
    return render(request, 'address/form.html', {
        'title': 'Create New City Municipality',
        'form': form,
    })

@login_required
def update_city_municipality(request, primary_key):
    city_municipality = get_object_or_404(City_Municipality, id = primary_key)

    if request.method == 'POST':
        form = CityMunicipalityForm(request.POST, instance=city_municipality)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successful! City Municipality has been updated.')
    else: 
        form = CityMunicipalityForm(instance=city_municipality)

    return render(request, 'address/form.html', {
        'title': 'Edit City Municipality',
        'form': form,
    })

@login_required
def create_barangay(request):
    if request.method == 'POST':
        form = BarangayForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successful! Barangay has been saved.')
    else:
        form = BarangayForm()
    
    return render(request, 'address/form.html', {
        'title': 'Create New Barangay',
        'form': form,
    })
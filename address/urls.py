from django.urls import path
from . import views

app_name = 'address'

urlpatterns = [
    path('region/', views.view_region, name='view_region'),
    path('region/create/', views.create_region, name='create_region'),
    path('region/update/<int:primary_key>/', views.update_region, name='update_region'),
    path('region/delete/<int:region_primary_key>/', views.delete_region, name='delete_region'),
    path('province/', views.view_province, name='view_province'),
    path('province/create/', views.create_province, name='create_province'),
    path('province/update/<int:primary_key>/', views.update_province, name='update_province'),
    path('city/create/', views.create_city_municipality, name='create_city_municipality'),
    path('city/update/<int:primary_key>/', views.update_city_municipality, name='update_city_municipality'),
    path('barangay/create/', views.create_barangay, name='create_barangay'),
    path('barangay/update/<int:primary_key>/', views.update_barangay, name='update_barangay'),
]
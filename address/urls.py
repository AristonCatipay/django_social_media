from django.urls import path
from . import views

app_name = 'address'

urlpatterns = [
    path('region/create/', views.create_region, name='create_region'),
    path('region/update/<int:primary_key>/', views.update_region, name='update_region'),
]
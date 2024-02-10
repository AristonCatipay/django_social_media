from django.urls import path
from . import views

app_name = 'address'

urlpatterns = [
    path('region/create/', views.create_region, name='create_region'),
]
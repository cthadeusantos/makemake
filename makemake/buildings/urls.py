from django.urls import path

from makemake.buildings.views import *

urlpatterns = [
    path('', home, name='home-buildings'),
    path('new/', new, name='new-buildings'),
    path('delete/<int:pk>/', delete, name='delete-building'),
    path('edit/<int:pk>/', edit, name='edit-building'),
]

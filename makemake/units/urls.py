from django.urls import path

from makemake.units.views import *

urlpatterns = [
    path('', home, name='home-units'),
    path('new/', new, name='new-units'),
    path('delete/<int:pk>/', delete, name='delete-unit'),
    path('edit/<int:pk>/', edit, name='edit-unit'),
    path('search/', search, name='search-units'),
]

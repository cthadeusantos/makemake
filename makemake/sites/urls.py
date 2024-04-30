from django.urls import path

from makemake.sites.views import *

urlpatterns = [
    path('', home, name='home-sites'),
    path('new/', new, name='new-sites'),
    path('delete/<int:pk>/', delete, name='delete-site'),
    path('edit/<int:pk>/', edit, name='edit-site'),
]

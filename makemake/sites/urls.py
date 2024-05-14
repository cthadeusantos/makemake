from django.urls import path

from makemake.sites.views import *

urlpatterns = [
    path('', home, name='home-sites'),
    path('void/', void, name='void'),
    path('new/', new, name='new-sites'),
    path('delete/<int:pk>/', delete, name='delete-site'),
    path('edit/<int:pk>/', edit, name='edit-site'),
    path('search/', search, name='search-sites'),
]

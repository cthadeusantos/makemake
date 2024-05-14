from django.urls import path

from makemake.companies.views import *

urlpatterns = [
    path('', home, name='home-companies'),
    path('void/', void, name='void'),
    path('new/', new, name='new-companies'),
    path('delete/<int:pk>/', delete, name='delete-company'),
    path('edit/<int:pk>/', edit, name='edit-company'),
    path('search/', search, name='search-companies'),
]

from django.urls import path

from makemake.agreements.views import *

urlpatterns = [
    #path('', home, name='home-agreements'),
    path('<int:pk>/', home, name='home-agreements'),
    path('new/<int:numproject>/', new, name='new-agreements'),
    path('delete/<int:pk>/', delete, name='delete-agreement'),
    path('search/', search, name='search-agreements'),
    path('edit/<int:pk>/', edit, name='edit-agreement'),
]

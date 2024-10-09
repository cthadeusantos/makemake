from django.urls import path

from makemake.imports.views import *

urlpatterns = [
    path('icompositions', icompositions, name='icompositions'),
    #path('new/', new, name='new-units'),
    #path('delete/<int:pk>/', delete, name='delete-unit'),
    #path('edit/<int:pk>/', edit, name='edit-unit'),
    #path('search/', search, name='search-units'),
]
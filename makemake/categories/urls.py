from django.urls import path

from makemake.categories.views import *

urlpatterns = [
    path('', home, name='home-categories'),
    path('new/', new, name='new-categories'),
    path('delete/<int:pk>/', delete, name='delete-category'),
    path('edit/<int:pk>/', edit, name='edit-category'),
]

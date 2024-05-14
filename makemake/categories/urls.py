from django.urls import path

from makemake.categories.views import *

urlpatterns = [
    path('', home, name='home-categories'),
    path('new/', add_or_edit, name='new-categories'),
    path('delete/<int:pk>/', delete, name='delete-category'),
    path('edit/<int:pk>/', add_or_edit, name='edit-category'),
    path('search/', search, name='search-categories'),
    path('details/<int:pk>/', details, name='details-category'),
]

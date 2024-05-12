from django.urls import path

from makemake.projects.views import *

urlpatterns = [
    path('', home, name='home-projects'),
    path('new/', new, name='new-project'),
    path('edit/<int:pk>/', edit2, name='edit-project'),
    path('delete/<int:pk>/', delete, name='delete-project'),
    path('details/<int:pk>/', details, name='details-project'),
    path('search/', search, name='search-projects'),
    #path('partial', partial, name='partial'),
    path('get-select-options/<int:pk>/', get_select_options, name='get_select_options'),
    path('get-select-users/', get_select_users, name='get_select_users'),
    #path('version/<int:pk>/', version, name='version-project'),
]

from django.urls import path

from makemake.compositions.views import *
#from makemake.agreements.views import home2

urlpatterns = [
    path('', home, name='home-compositions'),
    path('new/', new, name='new-composition'),
    path('duplicate/<int:pk>/', duplicate, name='duplicate-composition'),
    path('edit/<int:pk>/', edit, name='edit-composition'),
    path('delete/<int:pk>/', delete, name='delete-composition'),
    path('details/<int:pk>/', details, name='details-composition'),
    path('prices/<int:pk>/', prices, name='prices-composition'),
    path('search/', search2, name='search-composition'),
    path('search_components', search_components, name='search_components'),
    # path('get-select-options/<int:pk>/', get_select_options, name='get_select_options'),
    # path('get-select-users/', get_select_users, name='get_select_users'),
]

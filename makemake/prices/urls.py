from django.urls import path

from makemake.prices.views import *

urlpatterns = [
    path('', home, name='home-prices'),
    #path('new/', new, name='new-units'),
    #path('delete/<int:pk>/', delete, name='delete-unit'),
    #path('edit/<int:pk>/', edit, name='edit-unit'),
    path('search-prices-labels/', search_prices_labels, name='search-prices-labels'),
]

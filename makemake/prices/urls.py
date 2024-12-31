from django.urls import path

from makemake.prices.views import *

urlpatterns = [
    path('', home, name='home-prices'),
    path('home_references/', home_references, name='home-references'),
    path('add_price/', new_prices, name='new-price'),
    path('add_reference/', add_or_edit_reference, name='new-reference'),
    path('edit_reference/<int:pk>/', add_or_edit_reference, name='edit-reference'),
    #path('new/', new, name='new-units'),
    path('delete/<int:pk>/', delete_reference, name='delete-reference'),
    #path('edit/<int:pk>/', edit, name='edit-unit'),
    path('search-prices-labels/', search_prices_labels, name='search-prices-labels'),
    #path('imports/', ImportPrices, name='import-prices'),
]

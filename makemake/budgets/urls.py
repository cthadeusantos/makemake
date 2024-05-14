from django.urls import path

from makemake.budgets.views import *

urlpatterns = [
    path('<int:pk>/', home, name='home-budgets'),
    path('add/', budget_view, name='add-budgets'),
    path('edit/<int:pk>/', add_or_edit, name='edit-budgets'),
    path('search-category/', search_categories, name='search-categories'),
    #path('void/', void, name='void'),
    #path('new/', new, name='new-sites'),
    #path('delete/<int:pk>/', delete, name='delete-site'),
    #path('edit/<int:pk>/', edit, name='edit-site'),
    #path('search/', search, name='search-sites'),
]
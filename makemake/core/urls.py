# makemake/core/urls.py
from django.urls import path

from makemake.core.views import *

    #path('', makemake.core.views.home, name=''),
    #path('', makemake.core.views.home, name='home'),
    #path('accounts/login/', makemake.core.views.login_initial, name='login'),
    #path('accounts/logout/', makemake.core.views.logout_user, name='logout'),
    #path('registration/', makemake.core.views.register, name='register'),

urlpatterns = [
    path('', home, name='home'),
    path('accounts/login/', login_initial, name='login'),
    path('accounts/logout/', logout_user, name='logout'),
    path('registration/', register, name='register'),
]
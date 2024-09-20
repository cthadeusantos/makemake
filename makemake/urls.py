"""
URL configuration for makemake project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import makemake.core.views
#import makemake.documents.views

urlpatterns = [
    #path('', makemake.core.views.home, name=''),
    #path('', makemake.core.views.home, name='home'),
    #path('accounts/login/', makemake.core.views.login_initial, name='login'),
    #path('accounts/logout/', makemake.core.views.logout_user, name='logout'),
    #path('registration/', makemake.core.views.register, name='register'),
    path('', include('makemake.core.urls')),
    path('agreements/', include('makemake.agreements.urls')),
    path('buildings/', include('makemake.buildings.urls')),
    path('categories/', include('makemake.categories.urls')),
    path('companies/', include('makemake.companies.urls')),
    path('compositions/', include('makemake.compositions.urls')),
    path('documents/', include('makemake.documents.urls')),
    path('projects/', include('makemake.projects.urls')),
    path('sites/', include('makemake.sites.urls')),
    path('budgets/', include('makemake.budgets.urls')),
    path('units/', include('makemake.units.urls')),
    path('prices/', include('makemake.prices.urls')),
    #path('documents/', makemake.documents.views.home),
    #path('documents/new/', makemake.documents.views.new),
    path('admin/', admin.site.urls),
]

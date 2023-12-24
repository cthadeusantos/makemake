from django.urls import path

from makemake.documents.views import *

urlpatterns = [
    path('<int:pk>/', home, name='home-documents'),
    path('new/<int:project_number>/', new, name='new-document'),
    path('edit/<int:pk>/<int:project_number>/', edit, name='edit-document'),
    path('delete/<int:pk>/', delete, name='delete-document'),
    path('details/<int:pk>/', details, name='details-document'),
    path('version/<int:pk>/', version, name='version-document'),
    path('download/<int:file_id>/', download_file, name='download-version-file'),
]

from django.urls import path

from makemake.documents.views import *

urlpatterns = [
    path('<int:pk>/', home, name='home-documents'),
    path('new/<int:numproject>/', new, name='new-document'),
    path('edit/<int:pk>/<int:numproject>/', edit, name='edit-document'),
    path('delete/<int:pk>/', delete, name='delete-document'),
    path('details/<int:pk>/', details, name='details-document'),
    path('version/<int:pk>/', version, name='version-document'),
    path('download/<int:file_id>/', download_file, name='download-version-file'),
    path('downloads/<int:numproject>/', download_files, name='download-document-files'),
]

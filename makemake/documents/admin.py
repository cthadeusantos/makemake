from django.contrib import admin

from makemake.documents.models import Document, Version


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'summary',
        'description',
        'created_at',
        'updated_at',
    )


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = (
        'version_number',
        'changelog',
        'upload_at',
        'upload_url',
    )

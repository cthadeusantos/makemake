from django.contrib import admin
from makemake.sites.models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'place',
    )
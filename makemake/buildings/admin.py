from django.contrib import admin

from makemake.buildings.models import Building


@admin.register(Building)
class BuldingAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'name',
        'status',
        'created_at',
        'updated_at',
    )
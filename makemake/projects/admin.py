from django.contrib import admin

from makemake.projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'description',
        'created_at',
    )
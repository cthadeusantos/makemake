from django.contrib import admin
from makemake.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'name',
        'description',
        'fordocs',
        'forbudgets',
    )

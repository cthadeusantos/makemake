from django.contrib import admin

from makemake.units.models import Unit

# Register your models here.
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'symbol_alternative1', 'symbol_alternative2', 'type', )
    list_filter = ('name',)
    search_fields = ('name',)
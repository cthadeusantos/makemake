from django.contrib import admin

from django.contrib import admin
from makemake.compositions.models import Composition

class CompositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'unit', 'type', 'iscomposition', 'discontinued', 'created_at', 'updated_at', 'dbtype')
    list_filter = ( 'type', 'iscomposition', 'discontinued', 'created_at', 'dbtype')
    search_fields = ( 'code', 'description',)
    ordering = ('code',)
    
    # Fields to be displayed when creating or editing an instance
    #fields = ('code', 'description', 'unit', 'type', 'settype', 'discontinued', 'create', 'compositions')
    fields = ( 'code', 'description', 'unit', 'type', 'iscomposition', 'discontinued', 'created_at', 'updated_at', 'dbtype')
    
    # Option to use a horizontal filter widget for ManyToMany fields
    #filter_horizontal = ('compositions',)
    
admin.site.register(Composition, CompositionAdmin)


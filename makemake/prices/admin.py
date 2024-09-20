from django.contrib import admin

from makemake.prices.models import PriceLabel

@admin.register(PriceLabel)
class PriceLabelAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'name',
        'date',
        'discontinued',
    )
    fields = ['reference', 'date', 'name', 'discontinued',]

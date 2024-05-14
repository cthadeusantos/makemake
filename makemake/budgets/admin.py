from django.contrib import admin

from makemake.budgets.models import PriceLabel

@admin.register(PriceLabel)
class PriceLabelAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'label',
        'date',
        'discontinued',
    )
    fields = ['reference', 'date', 'label', 'discontinued',]
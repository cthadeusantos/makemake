from django.forms import ModelForm, forms

from makemake.units.models import Unit

from makemake.core.tailwind_classes import CSS_CHARFIELD_1, CSS_SELECT_1

class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = [
            'symbol',
            'symbol_alternative1',
            'symbol_alternative2',
            'name',
            'type'
        ]
        labels = {
            'symbol': 'Symbol',
            'symbol_alternative1': 'Symbol Alternative 1',
            'symbol_alternative2': 'Symbol Alternative 2',
            'name': 'Unit',
            'type': 'Type'
        }
    
    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        super(UnitForm, self).__init__(*args, **kwargs)
        self.fields['symbol'].widget.attrs['class'] = CSS_CHARFIELD_1
        self.fields['name'].widget.attrs['class'] = CSS_CHARFIELD_1
        self.fields['type'].widget.attrs['class'] = CSS_SELECT_1
        if prefix == 'edit':
            self.fields['name'].initial = instance.name
            self.fields['symbol'].initial = instance.symbol
            self.fields['symbol_alternative1'].initial = instance.symbol_alternative1
            self.fields['symbol_alternative2'].initial = instance.symbol_alternative2
            self.fields['type'].initial = instance.type
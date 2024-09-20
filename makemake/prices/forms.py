from datetime import datetime
from django import forms
from django.forms import ValidationError, formset_factory, ChoiceField

from makemake.compositions.models import Composition

from makemake.core.tailwind_classes import *
from makemake.core.choices import PLACES_CHOICES

def validate_only_numbers(value):
    if not value.isdigit():
        raise ValidationError('This field accepts only numbers.')

class PriceForm(forms.Form):
    composition = forms.ModelChoiceField(
        queryset=Composition.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': CSS_SELECT_1,
                                   'id': 'select-component',
                                   }),
        label='Price'
    )
    price = forms.DecimalField( max_digits=11,
                                  decimal_places=2,
                                  widget=forms.NumberInput(
                                      attrs={'class': 'flex flex-col w-1/12 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 text-right',
                                             }))
    date = forms.DateField(label='Date',
                            widget=forms.DateInput(attrs={'type': 'date',
                                                          'class': CSS_CHARFIELD_1,
                                                          'readonly': 'true',
                                                          }))
    place = ChoiceField(label='Place',
                            choices=PLACES_CHOICES,
                            required=False,
                            widget=forms.Select(attrs={'class': CSS_SELECT_1}))
    burdened = forms.BooleanField(label='Burdened',
                                  widget=forms.CheckboxInput(
                                      attrs={'class': 'form-checkbox mb-3 h-4 w-4 text-blue-600'}),
                                      required=False)
    discontinued = forms.BooleanField(label='Discontinued',
                                      widget=forms.CheckboxInput(
                                          attrs={'class': 'form-checkbox mb-3 h-4 w-4 text-blue-600'}),
                                          required=False)
        
    def __init__(self, *args, **kwargs):
        super(PriceForm, self).__init__(*args, **kwargs)
        today_is = datetime.today
        self.fields['quantity'].initial = 0.0
        self.fields['date'].initial = today_is
        
PriceFormset = formset_factory(form=PriceForm, extra=1,)
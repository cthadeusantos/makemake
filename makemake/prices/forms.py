from datetime import datetime
from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ValidationError, formset_factory, ChoiceField
from django.forms.utils import ErrorList

from makemake.compositions.models import Composition
from makemake.prices.models import Price, PriceLabel


from makemake.core.tailwind_classes import *
from makemake.core.choices import PLACES_CHOICES

def validate_only_numbers(value):
    if not value.isdigit():
        raise ValidationError('This field accepts only numbers.')

class PriceLabelForm(forms.ModelForm):
    class Meta:
        model = PriceLabel
        fields = ['name', 'reference', 'discontinued']
        widgets ={
            'name': forms.Textarea(attrs={
                'rows': 1,
                'cols': 100,
                'style': 'resize:vertical',
                'class': 'flex flex-col w-1/2 flex-1 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                #'readonly': 'readonly',
            }),
            'reference': forms.DateInput(attrs={
                    'class': CSS_CHARFIELD_1,
                    #'readonly': 'false',
                    }),
            'discontinued': forms.CheckboxInput(
                    attrs={'class': 'form-checkbox mb-3 h-4 w-4 text-blue-600'
                           }),
        }
    def __init__(self, *args, **kwargs):
        #prefix = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        super(PriceLabelForm, self).__init__(*args, **kwargs)
        if instance is not None:
            is_exist = Price.objects.filter(label=instance).exists()

            #self.fields['name'].widget.attrs['readonly'] = True
            self.fields['name'].initial = instance.name
            self.fields['reference'].initial = instance.reference
            self.fields['discontinued'].initial = instance.discontinued

            # Falta montar os casos que são permitidos ou não editar os campos
            # Por enquanto, unica opção é se o registro já foi usado em Price
            # não permite editar 2 campos
            #self.fields['name'].widget.attrs['disabled'] = True
            if is_exist == True or instance.discontinued == True:
                self.fields['reference'].widget.attrs['readonly'] = True
                #self.fields['discontinued'].widget.attrs['disabled'] = True
            if instance.discontinued == True:
                self.fields['discontinued'].widget.attrs['disabled'] = True
            #     self.fields['reference'].widget.attrs['readonly'] = True

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

class ImportPricesForm(forms.Form):
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
    upload_url = forms.FileField(label='File',
                                 widget=forms.FileInput(attrs={'name': 'file',
                                                               'readonly': 'true',
                                                               'class': CSS_SELECT_1,
                                                               }))
        
    def __init__(self, *args, **kwargs):
        super(ImportPricesForm, self).__init__(*args, **kwargs)
        today_is = datetime.today
        self.fields['date'].initial = today_is
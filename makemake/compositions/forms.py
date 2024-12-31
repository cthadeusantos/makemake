from django import forms
from datetime import datetime
import re

from django.forms import ChoiceField, ValidationError, formset_factory, inlineformset_factory, modelformset_factory
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.db.models import Max, Q


from makemake.buildings.forms import SelectBuildingForm

from makemake.projects.models import Project
from makemake.buildings.models import Building
from makemake.units.models import Unit
from makemake.compositions.models import Composition
from makemake.prices.models import PriceLabel, Price

from makemake.core.choices import PROJECT_STATUS_CHOICES, TYPE_COMPOSITION_CHOICES, BUDGETS_DATABASES_CHOICES, PRICE_TYPE_CHOICES, PLACES_CHOICES
from makemake.core.tailwind_classes import *

def validate_only_numbers(value):
    if not value.isdigit():
        raise ValidationError('This field accepts only numbers.')
    
def validate_value(value):
    # Expressão regular para validar o formato XXXXXXXX.XX
    #pattern = r'^\d{8}\.\d{2}$'

    # Expressão regular para validar o formato X a XXXXXXXX seguido ou não por .XX
    pattern = r'^\d{1,8}(\.\d{2})?$'

    if not re.match(pattern, value):
        raise ValidationError('The value must be XXXXXXXX.XX.')


class CompositionForm(forms.Form):
    dbtype = forms.ChoiceField(choices = BUDGETS_DATABASES_CHOICES,
                               required=True,
                               widget=forms.Select(attrs={'class': CSS_SELECT_1,
                                                          }),
                                                          label='Database type')
    code = forms.CharField(label='Code',
                           required=True,
                           validators=[validate_only_numbers],
                           widget=forms.NumberInput(attrs={
                               'class': CSS_CHARFIELD_1,
                               }))
    description = forms.CharField(label='Description',
                                widget=forms.Textarea(attrs={
                                                            'rows': 3,
                                                            'cols': 100,
                                                            'style': 'resize:none',
                                                            'class': CSS_TEXTFIELD_1,
                                                            }))
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': CSS_SELECT_1,
                                   }),
        label='Unit'
    )
    type = forms.ChoiceField(choices = TYPE_COMPOSITION_CHOICES,
                             widget=forms.Select(attrs={'class': CSS_SELECT_1,
                                                        }),
                                                        label='type')

    iscomposition = forms.BooleanField(label='Composition',
                                       widget=forms.CheckboxInput(
                                           attrs={'class': 'form-checkbox mb-3 h-4 w-4 text-blue-600',}),
                                           required=False)
    discontinued = forms.BooleanField(label='Discontinued',
                                      widget=forms.CheckboxInput(
                                          attrs={'class': 'form-checkbox mb-3 h-4 w-4 text-blue-600'}),
                                          required=False)
    created_at = forms.DateField(label='Created at',
                                 widget=forms.DateInput(attrs={'type': 'date',
                                                               'class': CSS_CHARFIELD_1,
                                                               'readonly': 'true',
                                                               }))
    updated_at = forms.DateField(label='Updated at',
                                 widget=forms.DateInput(attrs={'type': 'date',
                                                               'readonly': 'true',
                                                               'class': CSS_CHARFIELD_1,
                                                               }))
    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        
        super(CompositionForm, self).__init__(*args, **kwargs)
        
        today_is = datetime.today
        
        if prefix == 'new' or prefix is None:
            self.fields['created_at'].initial = today_is
            self.fields['updated_at'].initial = today_is
            # Get Composition instance with max code
            max_code = Composition.objects.annotate(
                code_as_int=Cast('code', IntegerField())
            ).filter(
                ~Q(code_as_int=None)
            ).aggregate(max_code_as_int=Max('code_as_int'))['max_code_as_int']

            if max_code:
                self.fields['code'].initial = max_code + 1
            else:
                self.fields['code'].initial = 1
        elif prefix == 'edit':
            self.fields['code'].initial = instance.code
            self.fields['description'].initial = instance.description
            self.fields['unit'].initial = instance.unit
            self.fields['type'].initial = instance.type
            self.fields['iscomposition'].initial = instance.iscomposition
            self.fields['dbtype'].initial = instance.dbtype
            self.fields['discontinued'].initial = instance.discontinued
            self.fields['created_at'].initial = instance.created_at
            self.fields['updated_at'].initial = today_is

            self.fields['code'].widget.attrs['disabled'] = True
            self.fields['created_at'].widget.attrs['disabled'] = True
            self.fields['updated_at'].widget.attrs['disabled'] = True
            self.fields['dbtype'].widget.attrs['disabled'] = True
            self.fields['iscomposition'].widget.attrs['disabled'] = False
            self.fields['type'].widget.attrs['disabled'] = True
            self.fields['unit'].widget.attrs['disabled'] = True

class ComponentForm(forms.Form):
    origin_choices = [
        (1, 'Allocation Factor'),
        (2, 'Collected'),
    ]
    id = forms.CharField(widget=forms.TextInput(attrs={#'disabled': 'disabled',
                                                            'class':'flex flex-col w-1/12 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                            }))
    dbtype = forms.ChoiceField(choices = BUDGETS_DATABASES_CHOICES,
                               required=True,
                               widget=forms.Select(attrs={'class': 'flex flex-col w-1/12 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                          #'disabled': 'disabled',
                                                          }),
                                                          )

    code = forms.CharField(required=True,
                        validators=[validate_only_numbers],
                        widget=forms.TextInput(attrs={
                            'class': 'flex flex-col w-1/12 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                            #'readonly': 'readonly',
                            }))
    description = forms.CharField(
                            widget=forms.Textarea(attrs={
                                                        'rows': 1,
                                                        'cols': 100,
                                                        'style': 'resize:vertical',
                                                        'class': 'flex flex-col w-1/2 flex-1 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                        #'readonly': 'readonly',
                                                        }))
    origin = forms.ChoiceField(choices=origin_choices,
                               widget=forms.Select(attrs={'class':'flex flex-col w-1/12 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                              }))
    quantity = forms.DecimalField( max_digits=7,
                                  decimal_places=12,
                                  widget=forms.NumberInput(
                                      attrs={'class': 'flex flex-col w-1/12 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 text-right',
                                             }))

class CompositionPriceForm(forms.Form):
    label = forms.ModelChoiceField(queryset=PriceLabel.objects.filter(Q(discontinued=False)),
                                   widget=forms.Select(attrs={
                                       'class': 'flex flex-col w-1/4 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                        #'disabled': 'disabled',
                                        }),
                                        )
    price = forms.CharField(required=True,
                        validators=[validate_value],
                        widget=forms.TextInput(attrs={
                            'class': 'flex flex-col w-1/4 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                            #'readonly': 'readonly',
                            }))
    burdened = forms.ChoiceField(choices = PRICE_TYPE_CHOICES,
                            required=True,
                            widget=forms.Select(attrs={'class': 'flex flex-col w-1/4 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                        #'disabled': 'disabled',
                                                        }),
                                                        )
    place = forms.ChoiceField(choices = PLACES_CHOICES,
                        required=True,
                        widget=forms.Select(attrs={'class': 'flex flex-col w-1/4 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                    #'disabled': 'disabled',
                                                    }),
                                                    )
    

# Crie um formset manualmente para o BookForm
CompositionPriceFormSet = formset_factory(CompositionPriceForm, extra=1,)  # `extra` define o número de formulários extras exibidos
from datetime import datetime
from django import forms
from django.forms import ValidationError, ModelForm, formset_factory, inlineformset_factory

from django.contrib.auth.models import User

from makemake.budgets.models import Budget
from makemake.agreements.models import Agreement
from makemake.categories.models import Category
from makemake.compositions.models import Composition

from makemake.core.tailwind_classes import *


def validate_only_numbers(value):
    if not value.isdigit():
        raise ValidationError('This field accepts only numbers.')

# class BudgetForm(forms.ModelForm):
#     class Meta:
#         model = Budget
#         fields = ("quantity", "date", "agreement")
#         #initial_fields = [100, datetime.today]

    # def __init__(self):
    #     #super(BudgetForm, self).__init__(*args, **kwargs)
    #     today_is = datetime.today
    #     self.fields['quantity'].initial = 100
    #     self.fields['date'].initial = today_is

class BudgetForm(forms.Form):
    # agreement = forms.ModelChoiceField(
    #     queryset=Agreement.objects.all(),
    #     required=True,
    #     widget=forms.Select(attrs={'class': CSS_SELECT_1,
    #                                }),
    #     label='Agreement'
    # )
    compositions = forms.ModelChoiceField(
        queryset=Composition.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': CSS_SELECT_1,
                                   'id': 'select-component',
                                   }),
        label='Composition'
    )
    quantity = forms.CharField(label='Quantity',
                        validators=[validate_only_numbers],
                        widget=forms.NumberInput(attrs={
                            'class': CSS_CHARFIELD_1,
                            'step' : 0.1,
                            }))
    date = forms.DateField(label='Date',
                            widget=forms.DateInput(attrs={'type': 'date',
                                                          'class': CSS_CHARFIELD_1,
                                                          'readonly': 'true',
                                                          }))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': CSS_SELECT_1,
                                   }),
        label='Category'
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': CSS_SELECT_1,
                                   }),
        label='User'
    )
        
    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        today_is = datetime.today
        self.fields['quantity'].initial = 0.0
        self.fields['date'].initial = today_is
        
# BudgetFormset = inlineformset_factory(Agreement,
#                                           Budget,
#                                           form=BudgetForm,
#                                           fields=('quantity', 'date'),
#                                           extra=1,
#                                           can_delete=True)

BudgetFormset = formset_factory(form=BudgetForm, extra=1,)
#BudgetFormSet = inlineformset_factory(form=BudgetForm, extra=1)

class ComponentForm(forms.Form):
    id = forms.CharField(widget=forms.TextInput(attrs={'disabled': 'disabled',
                                                            'class':'flex flex-col mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                            }))
    dbtype = forms.CharField(widget=forms.TextInput(attrs={'disabled': 'disabled',
                                                        'class':'flex flex-col mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                        }))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': CSS_SELECT_1,
                                   #'readonly': 'readonly',
                                   }),
        label='Category'
    )
    composition =  forms.CharField(
                            widget=forms.Textarea(attrs={
                                                        'rows': 1,
                                                        #'cols': 100,
                                                        'style': 'resize:vertical',
                                                        'class': 'flex flex-col flex-1 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                        'readonly': 'readonly',
                                                        }))
    quantity = forms.CharField(label='Quantity',
                    validators=[validate_only_numbers],
                    widget=forms.NumberInput(attrs={
                        'class': CSS_CHARFIELD_1,
                        'step' : 0.1,
                        }))
    unit = forms.CharField(label='Unit',
                widget=forms.TextInput(attrs={
                    'disabled': 'disabled',
                    'class':'flex flex-col mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                    #'step' : 0.1,
                    }))
    # user = forms.ModelChoiceField(
    #     queryset=User.objects.all(),
    #     required=True,
    #     widget=forms.Select(attrs={'class': CSS_SELECT_1,
    #                                'disabled': 'disabled',
    #                                }),
    #     label='User'
    # )
    user = forms.CharField(widget=forms.TextInput(attrs={'disabled': 'disabled',
                                                        'class':'flex flex-col mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                        }))

    userid = forms.CharField(widget=forms.NumberInput(attrs={#'disabled': 'disabled',
                                                    'class':'flex flex-col mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                                                    }))
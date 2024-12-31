from datetime import datetime
from django import forms
from django.forms import ChoiceField

from makemake.core.tailwind_classes import *
from makemake.core.choices import PLACES_CHOICES

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
                                                               'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
                                                               'type': 'file',
                                                               }))
        
    def __init__(self, *args, **kwargs):
        super(ImportPricesForm, self).__init__(*args, **kwargs)
        today_is = datetime.today
        self.fields['date'].initial = today_is
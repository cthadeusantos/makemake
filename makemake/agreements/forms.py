from django import forms
from datetime import datetime, timedelta

from django.forms import formset_factory, inlineformset_factory
from django.forms import ModelChoiceField, ChoiceField

from makemake.core.choices import AGREEMENT_CATEGORIES_CHOICES

from makemake.documents.models import Document, Version
from makemake.projects.models import Project
from makemake.agreements.models import Agreement
from makemake.buildings.models import Building
from makemake.core.tailwind_classes import *

class AgreementForm(forms.Form):

    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={'name': 'description',
                                                               'rows': 3,
                                                               'cols': 100,
                                                               'style': 'resize:none',
                                                               'class': CSS_TEXTFIELD_1,
                                                               }))
    category = ChoiceField(choices=AGREEMENT_CATEGORIES_CHOICES, required=True, label="Agreement category", widget=forms.Select(attrs={'class': CSS_SELECT_1}))
    start = forms.DateField(label='Start',
                            widget=forms.DateInput(attrs={'name': 'start',
                                                            'type': 'date',
                                                            'class': CSS_SELECT_1,
                                                            #'readonly': 'false',
                                                            }))
    end = forms.DateField(label='End',
                          widget=forms.DateInput(attrs={'name': 'end',
                                                            'type': 'date',
                                                            'class': CSS_SELECT_1,
                                                            #'readonly': 'false',
                                                            }))
    project = forms.IntegerField(label="Number",
                                 widget=forms.NumberInput(attrs={'name': 'number',
                                                                 'type': 'hidden',
                                                                 'class': CSS_CHARFIELD_1,
                                                                 'readonly': 'true',
                                                                }))
    def __init__(self, *args, **kwargs):
        value = kwargs.pop('numproject', None)
        string = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        self.id_building = kwargs.pop('building', None)
        super(AgreementForm, self).__init__(*args, **kwargs)
        if string == 'new':
            self.fields['start'].initial = datetime.today()
            self.fields['end'].initial = datetime.today() + timedelta(days=90)
            self.fields['project'].initial = value
        elif string == 'edit':
            self.fields['description'].initial = instance.description
            self.fields['category'].initial = instance.category
            self.fields['start'].initial = instance.start
            self.fields['end'].initial = instance.end
            self.fields['project'].initial = value
            
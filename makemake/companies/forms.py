from django import forms
from datetime import datetime

from django.forms import ChoiceField, formset_factory, inlineformset_factory, modelformset_factory
from django.shortcuts import render
from django.contrib.auth.models import User

from makemake.companies.models import Company
from makemake.core.choices import PROJECT_STATUS_CHOICES
from makemake.core.tailwind_classes import *


class CompanyForm(forms.Form):
    name = forms.CharField(label='Company name', widget=forms.TextInput(attrs={'name': 'name',
                                                               'style': 'resize:none',
                                                               'class': CSS_TEXTFIELD_1,
                                                               }),
                                                               max_length=200,
                                                               )
    number = forms.CharField(label='Company number', widget=forms.TextInput(attrs={'name': 'number',
                                                                                   'style': 'resize:none',
                                                                                   'class': CSS_TEXTFIELD_1,
                                                                                   }),
                                                                                   max_length=14,)
    def __init__(self, *args, **kwargs):
        string = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        self.id_building = kwargs.pop('building', None)
        super(CompanyForm, self).__init__(*args, **kwargs)
        if string == 'new':
            # self.fields['building'].queryset = Building.objects.filter(buildings__id=value)
            # self.fields['categories'].queryset = Category.objects.all()
            # self.fields['created_at'].initial = datetime.today()
            # self.fields['updated_at'].initial = datetime.today()
            pass
        elif string == 'edit':
            self.fields['name'].initial = instance.name
            self.fields['number'].initial = instance.number
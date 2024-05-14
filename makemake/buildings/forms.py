from django import forms
from django.forms import formset_factory, inlineformset_factory
from makemake.buildings.models import Building
from makemake.sites.models import Site

from makemake.projects.models import Project
from django.forms import ChoiceField

from datetime import datetime

from makemake.core.choices import BUILDING_STATUS_CHOICES
from makemake.core.tailwind_classes import *

class SelectBuildingForm(forms.Form):
    building = forms.ModelChoiceField(
        queryset=Building.objects.all(),
        required=False,
        label='Building',
    )

class BuildingForm(forms.Form):
    name = forms.CharField(label='Name',
                              widget=forms.Textarea(attrs={'name': 'summary','rows': 2,
                                                           'cols': 100,
                                                           'style': 'resize:none',
                                                           'class': CSS_TEXTFIELD_1,
                                                           }),
                                                           max_length=100,
                                                           )
    number = forms.IntegerField(label="Number",
                                widget=forms.NumberInput(attrs={'name': 'number',
                                                                'type': 'number',
                                                                'class': CSS_CHARFIELD_1,
                                                                }))
    #status = forms.IntegerField()
    site = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': CSS_SELECT_1, 'readonly': 'readonly',}),
        label='Site'
    )
    status = ChoiceField(choices=BUILDING_STATUS_CHOICES, required=True, label="Status", widget=forms.Select(attrs={'class': CSS_SELECT_1}))
    created_at = forms.DateField(label='Created date',
                                 widget=forms.DateInput(attrs={'name': 'created_at',
                                                               'type': 'date',
                                                               'class': CSS_CHARFIELD_1,
                                                               'readonly': 'True',
                                                               }))
    updated_at = forms.DateField(label='Updated date',
                                 widget=forms.DateInput(attrs={'name': 'updated_at',
                                                               'type': 'date',
                                                               'class': CSS_CHARFIELD_1,
                                                               'readonly': 'True'
                                                               }))
    
    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        super(BuildingForm, self).__init__(*args, **kwargs)
        today_is = datetime.today
        if prefix == 'new':
            self.fields['created_at'].initial = today_is
            self.fields['updated_at'].initial = today_is
        elif prefix == 'edit':
            self.fields['name'].initial = instance.name
            self.fields['number'].initial = instance.number
            self.fields['status'].initial = instance.status
            self.fields['site'].initial = instance.site
            self.fields['created_at'].initial = instance.created_at
            self.fields['updated_at'].initial = today_is

            self.fields['number'].widget.attrs['readonly'] = True
            self.fields['site'].widget.attrs['disabled'] = True

            
from django import forms
from django.forms import formset_factory, inlineformset_factory
from makemake.buildings.models import Building
from makemake.projects.models import Project
from django.forms import ChoiceField

from datetime import datetime

from makemake.core.choices import BUILDING_STATUS_CHOICES

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
                                                           'class': 'form-control form-control-sm',
                                                           }))
    number = forms.IntegerField(label="Number",
                                widget=forms.NumberInput(attrs={'name': 'number',
                                                                'type': 'number',
                                                                'class': 'form-control form-control-sm',
                                                                }))
    #status = forms.IntegerField()
    status = ChoiceField(choices=BUILDING_STATUS_CHOICES, required=True, label="Status", widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    created_at = forms.DateField(label='Created date',
                                 widget=forms.DateInput(attrs={'name': 'created_at',
                                                               'type': 'date',
                                                               'class': 'form-control form-control-sm',
                                                               'readonly': 'True',
                                                               }))
    updated_at = forms.DateField(label='Updated date',
                                 widget=forms.DateInput(attrs={'name': 'updated_at',
                                                               'type': 'date',
                                                               'class': 'form-control form-control-sm',
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
            self.fields['created_at'].initial = instance.created_at
            self.fields['updated_at'].initial = today_is

            self.fields['number'].widget.attrs['readonly'] = True
        else:
            self.fields['name'].initial = self.name
            self.fields['number'].initial = self.number
            self.fields['status'].initial = self.status
            self.fields['created_at'].initial = self.created_at
            self.fields['updated_at'].initial = self.updated_at

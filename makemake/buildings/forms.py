from django import forms
from django.forms import formset_factory, inlineformset_factory
from makemake.buildings.models import Building
from makemake.projects.models import Project

class SelectBuildingForm(forms.Form):
    building = forms.ModelChoiceField(
        queryset=Building.objects.all(),
        required=False,
        label='Building',
    )

class BuildingForm(forms.Form):
    name = forms.CharField(label='Project name', max_length=200)
    number = forms.IntegerField()
    status = forms.IntegerField()
    created_at = forms.DateField(label='Created at',
                                 widget=forms.DateInput(attrs={'name': 'created_at',
                                                               'type': 'date'}))
    updated_at = forms.DateField(label='Updated at',
                                 widget=forms.DateInput(attrs={'name': 'updated_at',
                                                               'type': 'date'}))



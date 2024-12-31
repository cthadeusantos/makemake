#from django.forms import ModelForm, Textarea, Select
from django import forms
from django.forms import ModelChoiceField, ChoiceField

from makemake.sites.models import Site
from makemake.buildings.models import Building

from makemake.core.choices import PLACES_CHOICES
from makemake.core.tailwind_classes import *

# class SiteForm(ModelForm):
#     class Meta:
#         model = Site
#         fields = [
#             'name',
#             'place',
#         ]
#         labels = {
#             'name': 'Site',
#             'place': 'Place',
#         }
#         widget = { 'name': Textarea(attrs={'name': 'name',
#                                            'rows': 1,
#                                            'cols': 100,
#                                            'style': 'resize:none',
#                                            'class': 'form-control form-control-sm',
#                                            'maxlenght': 100,
#                                            }),
#                     'place': Select(attrs={'class': 'form-select form-select-sm'}),
#                 }
        
class SiteForm(forms.Form):
    name = forms.CharField(label='Name',
                               widget=forms.Textarea(attrs={'name': 'name','rows': 1,
                                                            'cols': 100,
                                                            'style': 'resize:none',
                                                            'class': CSS_CHARFIELD_1,
                                                            }),
                                                            max_length=100,
                                                            )
    place = ChoiceField(label='Place',
                             choices=PLACES_CHOICES,
                             required=False,
                             widget=forms.Select(attrs={'class': CSS_SELECT_1}))
    
    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        super(SiteForm, self).__init__(*args, **kwargs)
        if prefix == 'edit':
            self.fields['name'].initial = instance.name
            self.fields['place'].initial = instance.place
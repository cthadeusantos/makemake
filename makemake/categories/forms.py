from django import forms
from django.forms import formset_factory, inlineformset_factory
from makemake.categories.models import Category
from makemake.documents.models import Document


class CategoryForm(forms.Form):
    code = forms.CharField(label='Code',
                               widget=forms.Textarea(attrs={'name': 'code','rows': 2,
                                                            'cols': 50,
                                                            'style': 'resize:none'
                                                            }))
    name = forms.CharField(label='Name',
                               widget=forms.Textarea(attrs={'name': 'name','rows': 2,
                                                            'cols': 50,
                                                            'style': 'resize:none'
                                                            }))
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={'name': 'description',
                                                               'rows': 2,
                                                               'cols': 50,
                                                               'style': 'resize:none'
                                                               }))
    # created_at = forms.DateField(label='Created at',
    #                              widget=forms.DateInput(attrs={'name': 'created_at',
    #                                                            'type': 'date'}))
    # updated_at = forms.DateField(label='Updated at',
    #                              widget=forms.DateInput(attrs={'name': 'updated_at',
    #                                                            'type': 'date'}))

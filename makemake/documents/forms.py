from django import forms
from datetime import datetime

from django.forms import formset_factory, inlineformset_factory
from django.forms import ModelChoiceField, ChoiceField

from makemake.core.choices import FILE_EXTENSION_CHOICES, DOCUMENT_STATUS_CHOICES

from makemake.documents.models import Document, Version
from makemake.projects.models import Project
from makemake.categories.models import Category
from makemake.buildings.models import Building
from makemake.core.tailwind_classes import *

class DocumentForm2(forms.Form):
    summary = forms.CharField(label='summary',
                              widget=forms.Textarea(attrs={'name': 'summary','rows': 2,
                                                           'cols': 50,
                                                           'style': 'resize:none',
                                                           'class': CSS_TEXTFIELD_1,
                                                           }))
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={'name': 'description',
                                                               'rows': 3,
                                                               'cols': 100,
                                                               'style': 'resize:none',
                                                               'class': CSS_TEXTFIELD_1,
                                                               }))
    created_at = forms.DateField(label='Created date',
                                 widget=forms.DateInput(attrs={'name': 'created_at',
                                                               'type': 'date',
                                                               'class': CSS_SELECT_1,
                                                               'readonly': 'true',
                                                               }))
    updated_at = forms.DateField(label='Updated date',
                                 widget=forms.DateInput(attrs={'name': 'updated_at',
                                                               'type': 'date',
                                                               'class': CSS_CHARFIELD_1,
                                                               'readonly': 'true'}))
    doctype = ChoiceField(choices=FILE_EXTENSION_CHOICES, required=True, label="Document type", widget=forms.Select(attrs={'class': CSS_SELECT_1}))
    docstatus = ChoiceField(choices=DOCUMENT_STATUS_CHOICES, required=True, label="Document status", widget=forms.Select(attrs={'class': CSS_SELECT_1}))
    building = ModelChoiceField(queryset=Building.objects.all(), required=True, widget=forms.Select(attrs={'class': CSS_SELECT_1}))
    categories = ModelChoiceField(queryset=Category.objects.all(), required=True, widget=forms.Select(attrs={'class': CSS_SELECT_1}))
    
    def __init__(self, *args, **kwargs):
        value = kwargs.pop('numproject', None)
        string = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        self.id_building = kwargs.pop('building', None)
        super(DocumentForm2, self).__init__(*args, **kwargs)
        if string == 'new':
            self.fields['building'].queryset = Building.objects.filter(buildings__id=value)
            self.fields['categories'].queryset = Category.objects.all()
            self.fields['created_at'].initial = datetime.today()
            self.fields['updated_at'].initial = datetime.today()
        elif string == 'edit':
            self.fields['summary'].initial = instance.summary
            self.fields['description'].initial = instance.description
            self.fields['building'].initial = instance.building.id
            self.fields['categories'].initial = instance.categories
            self.fields['created_at'].initial = instance.created_at
            self.fields['updated_at'].initial = datetime.today()
            self.fields['doctype'].initial = instance.doctype
            self.fields['docstatus'].initial = instance.docstatus
            self.fields['building'].disabled = True
            self.fields['categories'].disabled = True
            

class VersionForm(forms.Form):
    version_number = forms.IntegerField(label='Version',
                                        widget=forms.NumberInput(attrs={'name': 'version',
                                                                        'readonly': 'true',
                                                                        'class': CSS_CHARFIELD_1,
                                                                        }))
    changelog = forms.CharField(label='Changelog',
                                widget=forms.Textarea(attrs={'name': 'changelog',
                                                             'rows': 3,
                                                             'cols': 100,
                                                             'style': 'resize:none',
                                                             'class': CSS_TEXTFIELD_1,
                                                             }))
    upload_at = forms.DateField(label='Upload date',
                                widget=forms.DateInput(attrs={'name': 'upload_at',
                                                              'type': 'date',
                                                              'readonly': 'true',
                                                              'class': CSS_CHARFIELD_1}))
    upload_url = forms.FileField(label='File',
                                 widget=forms.FileInput(attrs={'name': 'file',
                                                               'readonly': 'true',
                                                               'class': CSS_CHARFIELD_1,
                                                               }))

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)
        today_is = datetime.today()
        document = Document.objects.get(pk=pk)
        version = Version.objects.filter(document=document).last()
        if version is None:
            self.fields['version_number'].initial = 1
        else:
            self.fields['version_number'].initial = version.version_number + 1
        self.fields['upload_at'].initial = today_is  # or timezone aware equivalent
        # Readonly fields
        #self.fields['upload_at'].disabled = True
        #self.fields['version_number'].disabled = True
        #self.fields['upload_url'].widget.attrs.update({'type': 'file'})

# class ComboboxCategoryForm(forms.Form):
#     category = forms.ModelChoiceField(
#         queryset=Category.objects.filter(category__isnull=True),
#         required=False,
#     )

# class ComboboxSubCategoryForm(forms.Form):
#     category = forms.ModelChoiceField(
#         queryset=Category.objects.filter(category__isnull=False),
#         required=False,
#     )

# class ComboboxBuildingForm(forms.Form):
#     building = forms.ModelChoiceField(
#         queryset=Building.objects.all(),
#         required=False,
#     )

# DocCategoryFormSet = formset_factory(ComboboxCategoryForm, extra=1)
# DocBuildingFormSet = formset_factory(ComboboxBuildingForm, extra=1)





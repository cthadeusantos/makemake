from django import forms
from datetime import datetime

from django.forms import formset_factory, inlineformset_factory
from django.forms import ModelChoiceField, ChoiceField

from makemake.core.choices import FILE_EXTENSION_CHOICES

from makemake.documents.models import Document, Version
from makemake.projects.models import Project
from makemake.categories.models import Category
from makemake.buildings.models import Building

class DocumentForm2(forms.Form):
    summary = forms.CharField(label='summary',
                              widget=forms.Textarea(attrs={'name': 'summary','rows': 2,
                                                           'cols': 50,
                                                           'style': 'resize:none',
                                                           'class': 'form-control form-control-sm',
                                                           }))
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={'name': 'description',
                                                               'rows': 3,
                                                               'cols': 100,
                                                               'style': 'resize:none',
                                                               'class': 'form-control form-control-sm',
                                                               }))
    created_at = forms.DateField(label='Created date',
                                 widget=forms.DateInput(attrs={'name': 'created_at',
                                                               'type': 'date',
                                                               'class': 'form-control form-control-sm',
                                                               }))
    updated_at = forms.DateField(label='Updated date',
                                 widget=forms.DateInput(attrs={'name': 'updated_at',
                                                               'type': 'date',
                                                               'class': 'form-control form-control-sm'}))
    doctype = ChoiceField(choices=FILE_EXTENSION_CHOICES, required=True, label="Document type", widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    building = ModelChoiceField(queryset=Building.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    categories = ModelChoiceField(queryset=Category.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    
    def __init__(self, *args, **kwargs):
        value = kwargs.pop('project_number', None)
        string = kwargs.pop('prefix', None)
        self.id_building = kwargs.pop('building', None)
        super(DocumentForm2, self).__init__(*args, **kwargs)
        if string == 'new':
            self.fields['building'].queryset = Building.objects.filter(buildings__id=value)
            self.fields['categories'].queryset = Category.objects.all()
            self.fields['created_at'].initial = datetime.today()
            self.fields['updated_at'].initial = datetime.today()
        elif string == 'repost':
            # Enabled fields
            self.fields['created_at'].readonly = False
            self.fields['updated_at'].readonly = False

class VersionForm(forms.Form):
    version_number = forms.IntegerField(label='Version',
                                        widget=forms.NumberInput(attrs={'name': 'version',
                                                                        'readonly': 'true',
                                                                        'class': 'form-control form-control-sm',
                                                                        }))
    changelog = forms.CharField(label='Changelog',
                                widget=forms.Textarea(attrs={'name': 'changelog',
                                                             'rows': 3,
                                                             'cols': 100,
                                                             'style': 'resize:none',
                                                             'class': 'form-control form-control-sm',
                                                             }))
    upload_at = forms.DateField(label='Upload date',
                                widget=forms.DateInput(attrs={'name': 'upload_at',
                                                              'type': 'date',
                                                              'readonly': 'true',
                                                              'class': 'form-control form-control-sm'}))
    upload_url = forms.FileField(label='File',
                                 widget=forms.FileInput(attrs={'name': 'file',
                                                               'readonly': 'true',
                                                               'class': 'form-control form-control-sm',
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





from django import forms
from datetime import datetime

from django.forms import formset_factory, inlineformset_factory
from django.forms import ModelChoiceField

from makemake.core.choices import FILE_EXTENSION_CHOICES

from makemake.documents.models import Document, Version
from makemake.projects.models import Project
from makemake.categories.models import Category
from makemake.buildings.models import Building

class DocumentForm2(forms.Form):
    summary = forms.CharField(label='summary',
                              widget=forms.Textarea(attrs={'name': 'summary','rows': 2,
                                                           'cols': 50,
                                                           'style': 'resize:none'
                                                           }))
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={'name': 'description',
                                                               'rows': 3,
                                                               'cols': 100,
                                                               'style': 'resize:none'
                                                               }))
    created_at = forms.DateField(label='Created at',
                                 widget=forms.DateInput(attrs={'name': 'created_at',
                                                               'type': 'date'}))
    updated_at = forms.DateField(label='Updated at',
                                 widget=forms.DateInput(attrs={'name': 'updated_at',
                                                               'type': 'date'}))
    building = ModelChoiceField(Building.objects.none())
    categories = ModelChoiceField(Category.objects.none())
    #doctype = forms.ChoiceField(choices=FILE_EXTENSION_CHOICES, required=True)
    #building = ModelChoiceField(Building.objects.prefetch_related('buildings').all())
    #building = forms.ModelChoiceField(choices=[(choice.pk, choice) for choice in Building.objects.all()])
    #building = forms.ChoiceField(choices=[(choice.pk, choice) for choice in Building.objects.all()])

    # def __init__(self, *args, **kwargs):
    #     self.fields['created_at'].initial = datetime.now()  # or timezone aware equivalent
    #     today_is = datetime.today()
    #     if instance is None:
    #         self.fields['created_at'].initial = today_is  # or timezone aware equivalent
    #         self.fields['updated_at'].initial = today_is  # or timezone aware equivalent
    #         self.fields['building'] = building
    #     else:
    #         self.fields['summary'].initial = instance.summary
    #         self.fields['description'].initial = instance.description
    #         self.fields['created_at'].initial = instance.created_at  # or timezone aware equivalent
    #         self.fields['updated_at'].initial = today_is # or timezone aware equivalent
    #         #self.fields['building'] = building

    #     # Readonly fields
    #     self.fields['created_at'].disabled = True
    #     self.fields['updated_at'].disabled = True
    
    def __init__(self, *args, **kwargs):
        value = kwargs.pop('project_number')
        super(DocumentForm2, self).__init__(*args, **kwargs)
        self.fields['building'].queryset = Building.objects.filter(buildings__id=value)
        self.fields['categories'].queryset = Category.objects.all()
        today_is = datetime.today()
        self.fields['created_at'].initial = today_is  # or timezone aware equivalent
        self.fields['updated_at'].initial = today_is  # or timezone aware equivalent



class DocumentForm(forms.Form):
    summary = forms.CharField(label='summary',
                              widget=forms.Textarea(attrs={'name': 'summary','rows': 2,
                                                           'cols': 50,
                                                           'style': 'resize:none'
                                                           }))
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={'name': 'description',
                                                               'rows': 3,
                                                               'cols': 100,
                                                               'style': 'resize:none'
                                                               }))
    created_at = forms.DateField(label='Created at',
                                 widget=forms.DateInput(attrs={'name': 'created_at',
                                                               'type': 'date'}))
    updated_at = forms.DateField(label='Updated at',
                                 widget=forms.DateInput(attrs={'name': 'updated_at',
                                                               'type': 'date'}))
    #doctype = forms.ChoiceField(choices=FILE_EXTENSION_CHOICES, required=True)
    #building = ModelChoiceField(Building.objects.prefetch_related('buildings').all())
    #building = forms.ModelChoiceField(choices=[(choice.pk, choice) for choice in Building.objects.all()])
    #building = forms.ChoiceField(choices=[(choice.pk, choice) for choice in Building.objects.all()])

    def __init__(self, *args, **kwargs):
        try:
            instance = kwargs.pop('instance')
        except KeyError:
            instance = None
        try:
            building = kwargs.pop('building')
        except KeyError:
            building = None
        super().__init__(*args, **kwargs)
        self.fields['created_at'].initial = datetime.now()  # or timezone aware equivalent
        today_is = datetime.today()
        if instance is None:
            self.fields['created_at'].initial = today_is  # or timezone aware equivalent
            self.fields['updated_at'].initial = today_is  # or timezone aware equivalent
            self.fields['building'] = building
        else:
            self.fields['summary'].initial = instance.summary
            self.fields['description'].initial = instance.description
            self.fields['created_at'].initial = instance.created_at  # or timezone aware equivalent
            self.fields['updated_at'].initial = today_is # or timezone aware equivalent
            #self.fields['building'] = building

        # Readonly fields
        self.fields['created_at'].disabled = True
        self.fields['updated_at'].disabled = True

    def new(self, context):
        data = self.cleaned_data
        formset = context['category_formset']
        project_number = context['project_number']
        instance_temp = Project.objects.get(id=project_number)
        instance_building = Building.objects.get(id=context['building'])
        instance = Document(summary=data['summary'],
                            description=data['description'],
                            created_at=data['created_at'],
                            updated_at=data['updated_at'],
                            #doctype=data['doctype'],
                            project=instance_temp,
                            building=instance_building,
                            )
        instance.save()
        for i, form in enumerate(formset):
            field_name = f"categories-{i}-category"
            instance_temp = Category.objects.get(pk=form.data[field_name])
            instance.categories.add(instance_temp)

    def update(self, context):
        data = self.cleaned_data
        instance = Document.objects.get(pk=pk)
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()


class ComboboxCategoryForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(category__isnull=True),
        required=False,
    )

class ComboboxSubCategoryForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(category__isnull=False),
        required=False,
    )

class ComboboxBuildingForm(forms.Form):
    building = forms.ModelChoiceField(
        queryset=Building.objects.all(),
        required=False,
    )

DocCategoryFormSet = formset_factory(ComboboxCategoryForm, extra=1)
DocBuildingFormSet = formset_factory(ComboboxBuildingForm, extra=1)


class VersionForm(forms.Form):
    version_number = forms.IntegerField(label='Version')
    changelog = forms.CharField(label='Changelog',
                                widget=forms.Textarea(attrs={'name': 'changelog',
                                                             'rows': 3,
                                                             'cols': 100,
                                                             'style': 'resize:none'
                                                             }))
    upload_at = forms.DateField(label='Upload at',
                                widget=forms.DateInput(attrs={'name': 'upload_at',
                                                              'type': 'date'}))
    upload_url = forms.FileField(label='File')

    def __init__(self, *args, **kwargs):
        if 'pk' not in kwargs:
            pk = None
        else:
            pk = kwargs.pop('pk')
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
        self.fields['upload_at'].disabled = True
        self.fields['version_number'].disabled = True
        self.fields['upload_url'].widget.attrs.update({'type': 'file'})

    def save(self, pk):
        data = self.cleaned_data
        document_instance = Document.objects.get(pk=pk)
        version = Version(version_number=data['version_number'],
                          changelog=data['changelog'],
                          upload_at=data['upload_at'],
                          upload_url=data['upload_url'],
                          document=document_instance)
        version.save()


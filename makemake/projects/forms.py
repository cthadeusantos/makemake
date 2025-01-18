from django import forms
from datetime import datetime

from django.forms import ChoiceField, formset_factory, inlineformset_factory, modelformset_factory
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.db.models import Max, Q

from makemake.buildings.forms import SelectBuildingForm
from makemake.projects.models import Project
from makemake.buildings.models import Building
from makemake.sites.models import Site
from makemake.core.choices import PROJECT_STATUS_CHOICES
from makemake.core.tailwind_classes import *


# def create_building_form(request):
#     form = SelectBuildingForm()
#     context = {
#         "form": form
#     }
#     return render(request, "partials/book_form.html", context)

class ProjectBuildingForm(forms.Form):
    building = forms.ModelChoiceField(
            queryset=Building.objects.none(),
            required=False,
            #label='Building',
            widget=forms.Select(attrs={'class': CSS_SELECT_1})
        )
    # def __init__(self, *args, **kwargs):
    #     try:
    #         siteID = kwargs.pop('siteID')
    #         super(ProjectBuildingForm, self).__init__(*args, **kwargs)
    # #         self.fields['building'].queryset = Building.objects.filter(site__id=siteID)
    # #         passagem = 0
    #     except:

class ProjectForm(forms.Form):
    code = forms.IntegerField(label='Code',
                                    widget=forms.NumberInput(attrs={'name': 'code',
                                                                    'class': CSS_CHARFIELD_1,     
                                                                    'readonly': 'true',
                                                                    }))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'name': 'year',
                                                              'class': CSS_CHARFIELD_1,
                                                              'readonly': 'true',
                                                              }))
    name = forms.CharField(label='Project name', widget=forms.TextInput(attrs={'name': 'name',
                                                               'style': 'resize:none',
                                                               'class': CSS_TEXTFIELD_1,
                                                               }),
                                                               max_length=200,
                                                               )
    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={'name': 'description',
                                                               'rows': 3,
                                                               'cols': 100,
                                                               'style': 'resize:none',
                                                               'class': CSS_TEXTFIELD_1,
                                                               }))
    created_at = forms.DateField(label='Created at',
                                 widget=forms.DateInput(attrs={'name': 'created_at',
                                                               'type': 'date',
                                                               'class': CSS_CHARFIELD_1,
                                                               'readonly': 'true',
                                                               }))
    updated_at = forms.DateField(label='Updated at',
                                 widget=forms.DateInput(attrs={'name': 'updated_at',
                                                               'type': 'date',
                                                               'readonly': 'true',
                                                               'class': CSS_CHARFIELD_1,
                                                               }))
    project_manager = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': CSS_SELECT_1,
                                   'name': 'project_manager'}),
        label='Project Manager'
    )
    project_manager_support = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': CSS_SELECT_1,
                                   'name': 'project_manager_support'}),
        label='Project Manager Support'
    )
    project_status = ChoiceField(choices=PROJECT_STATUS_CHOICES, required=True, label="Project status", widget=forms.Select(attrs={'class': CSS_SELECT_1}))
    site = forms.ModelChoiceField(
            queryset=Site.objects.all(),
            required=True,
            widget=forms.Select(attrs={'class': CSS_SELECT_1, 'readonly': 'readonly',}),
            label='Site'
        )
    remarks = forms.CharField(label='Remarks',
                                    widget=forms.Textarea(attrs={'name': 'remarks',
                                                            'rows': 2,
                                                            'cols': 100,
                                                            'style': 'resize:none',
                                                            'class': CSS_TEXTFIELD_1,
                                                            }),
                                    required=False,
                                    )
    interlocutor = forms.CharField(label='Interlocutor',
                                    widget=forms.Textarea(attrs={'name': 'interlocutor',
                                                            'rows': 2,
                                                            'cols': 100,
                                                            'style': 'resize:none',
                                                            'class': CSS_TEXTFIELD_1,
                                                            }),
                                    required=False,
                                    )

    def __init__(self, *args, **kwargs):
        prefix = kwargs.pop('prefix', None)
        instance = kwargs.pop('instance', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        today_is = datetime.today
        year = datetime.now().year
        if prefix == 'new':
            self.fields['created_at'].initial = today_is
            self.fields['updated_at'].initial = today_is
            self.fields['year'].initial = year
            #query = Project.objects.filter(year=year).order_by('-code').first()

            # Get Project instance with max code
            max_code = Project.objects.annotate(
                code_as_int=Cast('code', IntegerField())
            ).filter(
                ~Q(code_as_int=None),
                year=year
            ).aggregate(max_code_as_int=Max('code_as_int'))['max_code_as_int']
            if max_code:
                self.fields['code'].initial = max_code + 1
            else:
                self.fields['code'].initial = 1
        elif prefix == 'edit':
            # Usando a instância para obter o ID do site default
            c_instances = [b_instance.site for b_instance in instance.buildings.all()]
            site_ID = c_instances[0].id
        
            # # Usando get para obter a instância de A
            # a_instance = Project.objects.get(pk=pk)

            # # Obtendo todos os elementos da tabela B relacionados com a instância de A
            # b_instances = a_instance.buildings.all()

            # # Obtendo todos os elementos da tabela B relacionados com a instância de A
            # d_instances = a_instance.members.all()

            # #site_pk = Site.objects.select_related('project__building').get(pk=1)
            # site_pk = c_instances[0].id - 1
            self.fields['code'].initial = instance.code
            self.fields['year'].initial = instance.year
            self.fields['name'].initial = instance.name
            self.fields['description'].initial = instance.description
            self.fields['created_at'].initial = instance.created_at
            self.fields['updated_at'].initial = today_is
            self.fields['project_manager'].initial = instance.project_manager
            self.fields['project_manager_support'].initial = instance.project_manager_support
            self.fields['project_status'].initial = instance.project_status
            self.fields['interlocutor'].initial = instance.interlocutor
            self.fields['remarks'].initial = instance.remarks
            self.fields['site'].initial = site_ID
            self.fields['site'].widget.attrs['disabled'] = True
            self.fields['site'].required = 'False'

# class ProjectBuildingForm(forms.Form):
#     building = forms.ModelChoiceField(queryset=Building.objects.none(),
#                                    widget=forms.Select(attrs={
#                                        'class': 'flex flex-col w-1/4 mr-2 p-2 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
#                                         #'disabled': 'disabled',
#                                         }),
#                                         )

# ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=1,)  # `extra` define o número de formulários extras exibidos


class UserForm(forms.Form):
    users = forms.ModelChoiceField(queryset=User.objects.all(),
                                   widget=forms.Select(attrs={'class': CSS_SELECT_1}))

class MembersForm(forms.Form):
    members = forms.ModelChoiceField(queryset=User.objects.all(),
                                     widget=forms.Select(attrs={'class': CSS_SELECT_1}))

class StakeholdersForm(forms.Form):
    stakeholders = forms.ModelChoiceField(queryset=User.objects.all(),
                                          widget=forms.Select(attrs={'class': CSS_SELECT_1}))

def set_MembersFormSet(project):
    members = project.members.all()
    num_elements = members.count()

    MembersFormSet = formset_factory(MembersForm)

    # Pega as chaves primárias da variável members
    initial_values = [{'members': value.pk} for value in members]     
    formset = MembersFormSet(initial=initial_values)

    # Define os campos como readonly
    for form in formset.forms:
        form.fields['members'].widget.attrs['disabled'] = True
        form.fields['members'].label = 'Member'
        form.fields['members'].label = False

    # Oculta o último campo
    #formset.forms[-1].fields['users'].widget.attrs['style'] = 'display: none;'

    # Oculta o último campo e seu rótulo
    formset.forms[-1].fields['members'].widget = forms.HiddenInput()

    return formset

def set_stakeholders_formset(project):
    stakeholders = project.stakeholders.all()
    num_elements = stakeholders.count()

    StakeholdersFormSet = formset_factory(StakeholdersForm)

    # Pega as chaves primárias da variável members
    initial_values = [{'stakeholders': value.pk} for value in stakeholders]     
    formset = StakeholdersFormSet(initial=initial_values)

    # Define os campos como readonly
    for form in formset.forms:
        form.fields['stakeholders'].widget.attrs['disabled'] = True
        form.fields['stakeholders'].label = 'Stakeholder'
        form.fields['stakeholders'].label = False

    # Oculta o último campo
    #formset.forms[-1].fields['users'].widget.attrs['style'] = 'display: none;'

    # Oculta o último campo e seu rótulo
    formset.forms[-1].fields['stakeholders'].widget = forms.HiddenInput()

    return formset

def set_buildings_formset(project):
    buildings = project.buildings.all()
    num_elements = buildings.count()

    BuildingsFormSet = formset_factory(ProjectBuildingForm)

    # Pega as chaves primárias da variável members
    initial_values = [{'building': value.pk} for value in buildings]     
    formset = BuildingsFormSet(initial=initial_values)

    # Define os campos como readonly
    for form in formset.forms:
        form.fields['building'].widget.attrs['disabled'] = True
        form.fields['building'].label = 'Building'
        form.fields['building'].label = False

    # Oculta o último campo
    #formset.forms[-1].fields['users'].widget.attrs['style'] = 'display: none;'

    # Oculta o último campo e seu rótulo
    formset.forms[-1].fields['building'].widget = forms.HiddenInput()

    return formset
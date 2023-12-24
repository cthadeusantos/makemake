from django import forms
from datetime import datetime

from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.shortcuts import render

from makemake.buildings.forms import SelectBuildingForm
from makemake.projects.models import Project
from makemake.buildings.models import Building
from makemake.sites.models import Site

from django.contrib.auth.models import User

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
            widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
        )
    # def __init__(self, *args, **kwargs):
    #     try:
    #         siteID = kwargs.pop('siteID')
    #         super(ProjectBuildingForm, self).__init__(*args, **kwargs)
    # #         self.fields['building'].queryset = Building.objects.filter(site__id=siteID)
    # #         passagem = 0
    #     except:

class ProjectForm(forms.Form):
    name = forms.CharField(label='Project name')
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
    site = forms.ModelChoiceField(
            queryset=Site.objects.all(),
            required=True,
            #label='site'
        )

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['created_at'].initial = datetime.today
        self.fields['created_at'].disabled = True
        self.fields['updated_at'].initial = datetime.today
        self.fields['updated_at'].disabled = True

class ProjectForm2(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description','created_at', 'updated_at']
        widgets = {'description': forms.Textarea(attrs={'name': 'description',
                                                        'rows': 3,
                                                        'cols': 100,
                                                        'style': 'resize:none'})}
        # site = forms.ModelChoiceField(queryset=Site.objects.all(),
        #                               to_field_name='name',
        #                               label='site',
        #                               required=True,
        #                               widget=forms.Select(attrs={'class': 'form-control'})
        #                               )


    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('pk')
        super(ProjectForm2, self).__init__(*args, **kwargs)
        site_queryset=Site.objects.all()
        # self.fields['created_at'].initial = datetime.today
        self.fields['created_at'].disabled = True
        self.fields['updated_at'].initial = datetime.today
        self.fields['updated_at'].disabled = True
        self.fields['site'] = forms.ModelChoiceField(queryset=site_queryset,
                                      to_field_name='pk',
                                      #label='site',
                                      required=True,
                                      widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
                                      )
        a_instance = Project.objects.prefetch_related('buildings__site').get(pk=pk)
        c_instances = [b_instance.site for b_instance in a_instance.buildings.all()]
    
        # Usando get para obter a instância de A
        a_instance = Project.objects.get(pk=pk)

        # Obtendo todos os elementos da tabela B relacionados com a instância de A
        b_instances = a_instance.buildings.all()

        # Obtendo todos os elementos da tabela B relacionados com a instância de A
        d_instances = a_instance.members.all()

        #site_pk = Site.objects.select_related('project__building').get(pk=1)
        site_pk = c_instances[0].id - 1
        self.fields['site'].queryset = site_queryset
        self.fields['site'].initial = site_queryset[site_pk]
        self.fields['site'].widget.attrs['disabled'] = True

class UserForm(forms.Form):
    users = forms.ModelChoiceField(queryset=User.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))

class MembersForm(forms.Form):
    members = forms.ModelChoiceField(queryset=User.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))

class StakeholdersForm(forms.Form):
    stakeholders = forms.ModelChoiceField(queryset=User.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))

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
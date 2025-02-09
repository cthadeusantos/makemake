import re
from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from makemake.sites.models import Site
from makemake.buildings.models import Building
from makemake.buildings.forms import BuildingForm, SelectBuildingForm
# from makemake.projects.forms import ProjectForm, ProjectBuildingForm, ProjectForm2, ProjectForm3
from makemake.projects.forms import ProjectForm, ProjectBuildingForm
from makemake.projects.models import Project
from makemake.projects.forms import UserForm, MembersForm, set_MembersFormSet, set_stakeholders_formset, set_buildings_formset
from makemake.documents.models import Document

from makemake.core.custom_functions import is_list_empty, separar_valores_com_espaco, separar_valores_sem_espaco, get_actor, create_or_update_object

from auditlog.context import set_actor
#from auditlog.models import LogEntry

from makemake.core.custom_functions import get_client_ip, is_queryset_empty
from makemake.projects.custom_functions import filter_dynamic_keys, save_m2m_relationships
#from makemake.projects.signals import log_m2m_changes


def void(request):
    return HttpResponseRedirect('')

def search(request):
    # Expressão regular
    # String de exemplo
    #string = "   123   /   456  "

    regex = r"^\s*(\d+)\s*\/\s*(\d+)\s*$"

    # Texto de consulta enviado através do formulário
    input_text = request.GET.get('search', None)

    if input_text == '' or input_text is None:
        items = Project.objects.all().order_by('-year','-code')
        return render(request, 'projects/home.html', {'items': items})

    # Verifica se a string corresponde ao padrão
    match = re.match(regex, input_text)

    if match: # Check if pattern is code / year
        x = int(match.group(1))  # Captura o valor de X
        y = int(match.group(2))  # Captura o valor de Y
        # Use Q objects para filtrar seu modelo
        items = Project.objects.filter(Q(code=x) & Q(year=y))
    else:   # Pattern is a free string
        and_list, or_list = separar_valores_sem_espaco(input_text)
        if is_list_empty(and_list) and is_list_empty(or_list):
            items = Project.objects.filter(Q(name__icontains=input_text)).order_by('-year','-code')
        else:
            ### FUNCAO ABAIXO NÃO ESTA FUNCIONANDO
            ### PRECISA REFATORAR PARA FICAR MUITO MELHOR
            string_and = ''
            string_or = ''
            pattern = 'Q(name__icontains='
            for index, value in enumerate(and_list):
                string_and += pattern + '"' + value + '"' + ')'
                if index + 1 != len(and_list):
                    string_and += ' & '
                
            for index, value in enumerate(or_list):
                string_or += pattern + '"' + value + '"' + ')'
                if index + 1 != len(or_list):
                    string_or += ' | '
            final_string = string_and + " | " + string_or        
            # if not is_list_empty(and_list) and not is_list_empty(or_list):
            #     final_string = string_and + " | " + string_or
            # elif not is_list_empty(and_list) and  is_list_empty(or_list):
            #     final_string = string_and
            # else:
            #     final_string = string_or
            if not is_list_empty(and_list) and  is_list_empty(or_list):
                final_string = string_and
            elif is_list_empty(and_list) and  not is_list_empty(or_list):
                final_string = string_or
            items = Project.objects.filter(eval(final_string)).order_by('-year','-code')
    return render(request, 'projects/home.html', {'items': items})

"""
Initial homepage projects
"""
def home(request):
    items = Project.objects.all().order_by('-year','-code')
    print(get_client_ip(request))
    return render(request, 'projects/home.html', {'items': items})

"""
Delete a project 
"""
def delete(request, pk):
    project = Project.objects.get(pk=pk)
    if is_queryset_empty(has_linked_documents(project)):
        try:
            with set_actor(request.user):
                project.delete()
                messages.success(request, f"Registro {project.name} apagado com sucesso.")
        except:
            messages.error(request, f"Não foi possível apagar o registro: {project.name}") 
    else:
        messages.error(request, f"Não foi possível apagar o registro: {project.name}")

    return home(request)

"""
Check if a project has linked documents
"""
def has_linked_documents(value):
    return Document.objects.select_related('project').filter(project=value)

def details(request, pk):
    # Get project
    project = Project.objects.get(pk=pk)

    # Format date 
    project.created_at = project.created_at.strftime('%Y-%m-%d')
    project.updated_at = project.updated_at.strftime('%Y-%m-%d')

    context = {'project': project}
    return render(request, 'projects/details.html', context)

"""
Função de apoio a consulta javascript
"""
def get_select_options(request, pk):
    # Simulando dados da opção do select da base de dados
    options = [
        {'value': '1', 'label': 'Opção 1'},
        {'value': '2', 'label': 'Opção 2'},
        # Adicione mais opções conforme necessário
    ]
    site = Site.objects.get(pk=pk)

    # Fetch data from the database
    queryset = Building.objects.filter(site=site)

    # Convert the queryset to a list of dictionaries
    options = [{'value': item.id, 'label': str(item)} for item in queryset]
    return JsonResponse({'options': options})

"""
Função de apoio a consulta javascript
"""
def get_select_users(request):
    # Simulando dados da opção do select da base de dados
    options = [
        {'value': '1', 'label': 'Opção 1'},
        {'value': '2', 'label': 'Opção 2'},
        # Adicione mais opções conforme necessário
    ]

    # Fetch data from the database
    queryset = User.objects.all()

    # Convert the queryset to a list of dictionaries
    options = [{'value': item.id, 'label': str(item)} for item in queryset]
    return JsonResponse({'options': options})

"""
Add new projects and your references
"""
def new(request, numproject=None):

    if request.method == 'POST':    # Newly filled form
        project_form = ProjectForm(request.POST, prefix='repost')

        if project_form.is_valid():
            data = {
                "code": project_form.cleaned_data['code'],
                "year": project_form.cleaned_data['year'],
                "name": project_form.cleaned_data['name'],
                "description": project_form.cleaned_data['description'],
                "created_at": project_form.cleaned_data['created_at'],
                "updated_at": project_form.cleaned_data['updated_at'],
                "site": project_form.cleaned_data['site'],
                "project_manager": project_form.cleaned_data['project_manager'],
                "project_manager_support": project_form.cleaned_data['project_manager_support'],
                "interlocutor":project_form.cleaned_data['interlocutor'],
                "remarks": project_form.cleaned_data['remarks'],
                "project_status": project_form.cleaned_data['project_status'],
            }

            dict_auxiliary = {'buildings': [], 'members': [], 'stakeholders': []}
            filter_dynamic_keys(r'dynamic_selects_\d+$', 'buildings', Building, request, dict_auxiliary)
            filter_dynamic_keys(r'dynamic_selects_members_\d+$', 'members', User, request, dict_auxiliary)
            filter_dynamic_keys(r'dynamic_selects_stakeholders_\d+$', 'stakeholders', User, request,  dict_auxiliary)

            # Define new code
            register = None
            # Verifica se já existe uma entrada com a mesma combinação de 'code' e 'year'
            a = data['code']
            while Project.objects.filter(code=data['code'], year=data['year']).exists():
                # Existe, tenta o próximo disponível
                a += 1
                register = a

            # save registers
            pk = None
            with set_actor(request.user):
                b2 = create_or_update_object(request, Project, data)

                items_m2m = {key: value for key, value in dict_auxiliary.items() if value}
                save_m2m_relationships(b2, items_m2m, get_actor(request))
                pk = b2.pk

            if pk is not None:
                # Mesmo código que o método details
                project = Project.objects.get(pk=pk) 
                context = {'project': project, 'register': register} 
                return render(request, 'projects/details.html', context)
            else:   # OOPS! Some error ocurred 
                project = Project()
                context = {'project': project, 'register': register}
                return render(request, 'page_error.html', context) 
    else: # Empty new form
        project_form = ProjectForm(prefix='new')

    context = {'project_form': project_form,
               'numproject': numproject,
               }
    return render(request, 'projects/new_or_edit.html', context)

def edit(request, pk=None):
    numproject = pk
    if request.method == 'POST':    # Newly filled form
        project_form = ProjectForm(request.POST, prefix='repost')
        
        chaves = request.POST.keys()    # Seleciona todas as chaves de request.POST

        #if project_form.is_valid() and building_formset.is_valid():
        if project_form.is_valid():
            data = {
                "code": project_form.cleaned_data['code'],
                "year": project_form.cleaned_data['year'],
                "name": project_form.cleaned_data['name'],
                "description": project_form.cleaned_data['description'],
                "updated_at": project_form.cleaned_data['updated_at'],
                "project_manager": project_form.cleaned_data['project_manager'],
                "project_manager_support": project_form.cleaned_data['project_manager_support'],
                "project_status": project_form.cleaned_data['project_status'],
                "interlocutor":project_form.cleaned_data['interlocutor'],
                "remarks": project_form.cleaned_data['remarks'],
            }

            # Update the OBJECT
            register = data['code']
            b2 = create_or_update_object(request, Project, data, pk)

            # Filter buildings
            # Usar expressão regular para selecionar as chaves desejadas
            dict_auxiliary = {'buildings': [], 'members': [], 'stakeholders': []}
            filter_dynamic_keys(r'dynamic_selects_\d+$', "buildings", Building, request, dict_auxiliary)
            filter_dynamic_keys(r'form-\d+-building$', "buildings", Building, request, dict_auxiliary)
            filter_dynamic_keys(r'dynamic_selects_members_\d+$', "members", User, request, dict_auxiliary)
            filter_dynamic_keys(r'form-\d+-members$', "members", User, request, dict_auxiliary)
            filter_dynamic_keys(r'dynamic_selects_stakeholders_\d+$', "stakeholders", User, request, dict_auxiliary)
            filter_dynamic_keys(r'form-\d+-stakeholders$', "stakeholders", User, request, dict_auxiliary)

            items_m2m  = dict()
            change = False
            for key, value in dict_auxiliary.items():
                for instance in dict_auxiliary[key]:
                    if key=='buildings':
                        queryset = Project.objects.get(pk=pk).buildings.filter(pk=instance.pk)
                    elif key=='members':
                        queryset = Project.objects.get(pk=pk).members.filter(pk=instance.pk)
                    elif key=='stakeholders':
                        queryset = Project.objects.get(pk=pk).stakeholders.filter(pk=instance.pk)
                    if not len(queryset):
                        if key not in items_m2m:
                            items_m2m[key]=list()
                        items_m2m[key].append(instance)
                        change = True
                    
            #items_m2m = {key: value for key, value in dict_auxiliary.items() if value} # Build dictionary with values formatted to 
            if change:
                save_m2m_relationships(b2, items_m2m, get_actor(request))
            pk = b2.pk

            # Mesmo código que o método details
            project = Project.objects.get(pk=pk) # Mesmo código que o método details
            context = {'project': project, 'register': register} # Mesmo código que o método details
            return render(request, 'projects/details.html', context) # Mesmo código que o método details

    else:
        instance = Project.objects.get(pk=numproject)
        project_form = ProjectForm(instance=instance, prefix='edit')
    
    project_profile = Project.objects.get(pk=numproject)
    members_formset = set_MembersFormSet(project_profile)
    stakeholders_formset = set_stakeholders_formset(project_profile)
    
    # Make selectbox
    siteID = project_profile.buildings.first().site.id 
    buildings_formset = set_buildings_formset(project_profile)
    criterion1 = Q(site_id=siteID)
    queryset = Building.objects.filter(criterion1)
    for form in buildings_formset.forms:
        form.fields['building'].queryset = queryset

    context = {'project_form': project_form, 'numproject': numproject,
               'buildings_formset': buildings_formset, 'members_formset': members_formset,
               'stakeholders_formset': stakeholders_formset,}
    return render(request, 'projects/new_or_edit.html', context)




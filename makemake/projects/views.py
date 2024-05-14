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
from makemake.documents.models import Document

from makemake.projects.forms import UserForm, MembersForm, set_MembersFormSet, set_stakeholders_formset, set_buildings_formset

from makemake.core.custom_functions import is_list_empty, separar_valores_com_espaco, separar_valores_sem_espaco


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


def home(request):
    items = Project.objects.all().order_by('-year','-code')
    return render(request, 'projects/home.html', {'items': items})


def delete(request, pk):
    project = Project.objects.get(pk=pk)
    condition1 = len(has_linked_documents(project))
    if condition1:
        return JsonResponse({'success': False})
    project.delete()
    return home(request)


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


# def partial(request):
#     extra_forms = 1  # You can set the initial number of forms here
#     ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)
#     building_formset = ProjectBuildingFormSet(prefix='building')
#     #building_formset = SelectBuildingForm()
#     context = {'building_formset': building_formset,}
#     return render(request, 'projects/partial_new.html', context)


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

def new(request, numproject=None):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)

    if request.method == 'POST':    # Newly filled form
        project_form = ProjectForm(request.POST, prefix='repost')

        #if project_form.is_valid() and building_formset.is_valid():
        if project_form.is_valid():
            a = project_form.cleaned_data['code']
            b = project_form.cleaned_data['year']
            c = project_form.cleaned_data['name']
            d = project_form.cleaned_data['description']
            e = project_form.cleaned_data['created_at']
            f = project_form.cleaned_data['updated_at']
            g = project_form.cleaned_data['site']
            h = project_form.cleaned_data['project_manager']
            i = project_form.cleaned_data['project_manager_support']
            j = project_form.cleaned_data['interlocutor']
            k = project_form.cleaned_data['remarks']
            l = project_form.cleaned_data['project_status']

            register = None
            # Verifica se já existe uma entrada com a mesma combinação de 'code' e 'year'
            while Project.objects.filter(code=a, year=b).exists():
                # Existe, tenta o próximo disponível
                a += 1
                register = a

            # Logica para gravar instância principal
            b2 = Project(code=a, year=b, name=c, description=d, created_at=e, updated_at=f, project_manager=h, project_manager_support=i, project_status=l, interlocutor=j, remarks=k)
            b2.save()

            # Save buildings
            counter = 1
            keys = set()
            while (value := request.POST.get('dynamic_selects_' + str(counter), '')) != '':
                if value not in keys:
                    # Logica para gravar
                    keys.add(value)
                    b2.buildings.add(Building.objects.get(pk=value))
                counter += 1
            
            # Save members
            counter = 1
            keys = set()
            while (value := request.POST.get('dynamic_selects_members_' + str(counter), '')) != '':
                if value not in keys:
                    # Logica para gravar
                    keys.add(value)
                    b2.members.add(User.objects.get(pk=value))
                counter += 1

            # Save stakeholders
            counter = 1
            keys = set()
            while (value := request.POST.get('dynamic_selects_stakeholders_' + str(counter), '')) != '':
                if value not in keys:
                    # Logica para gravar
                    keys.add(value)
                    b2.stakeholders.add(User.objects.get(pk=value))
                counter += 1
            
            pk = b2.pk

            # Mesmo código que o método details
            project = Project.objects.get(pk=pk) # Mesmo código que o método details
            context = {'project': project, 'register': register} # Mesmo código que o método details
            return render(request, 'projects/details.html', context) # Mesmo código que o método details

    else: # Empty new form
        project_form = ProjectForm(prefix='new')

    context = {'project_form': project_form, 'numproject': numproject}
    return render(request, 'projects/new.html', context)

def new2(request, numproject=None):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)

    if request.method == 'POST':    # Newly filled form
        project_form = ProjectForm(request.POST, prefix='repost')

        chaves = request.POST.keys()    # Seleciona todas as chaves de request.POST

        #if project_form.is_valid() and building_formset.is_valid():
        if project_form.is_valid():
            a = project_form.cleaned_data['code']
            b = project_form.cleaned_data['year']
            c = project_form.cleaned_data['name']
            d = project_form.cleaned_data['description']
            e = project_form.cleaned_data['created_at']
            f = project_form.cleaned_data['updated_at']
            g = project_form.cleaned_data['site']
            h = project_form.cleaned_data['project_manager']
            i = project_form.cleaned_data['project_manager_support']
            j = project_form.cleaned_data['interlocutor']
            k = project_form.cleaned_data['remarks']
            l = project_form.cleaned_data['project_status']

            register = None
            # Verifica se já existe uma entrada com a mesma combinação de 'code' e 'year'
            while Project.objects.filter(code=a, year=b).exists():
                # Existe, tenta o próximo disponível
                a += 1
                register = a

            # Logica para gravar instância principal
            b2 = Project(code=a, year=b, name=c, description=d, created_at=e, updated_at=f, project_manager=h, project_manager_support=i, project_status=l, interlocutor=j, remarks=k)
            b2.save()

            # Save buildings
            keys = set()
            query = list(b2.buildings.values_list('id', flat=True))
            for id in query:
                keys.add(id)
            
            # Usar expressão regular para selecionar as chaves desejadas
            chaves_selecionadas = [chave for chave in chaves if re.match(r'form-\d+-building', chave)]
            for value in chaves_selecionadas:
                value = int(request.POST.get(value,''))
                if value not in keys:
                    # Logica para gravar
                    keys.add(value)
                    b2.buildings.add(Building.objects.get(pk=value))
            
            # Save members
            keys = set()
            query = list(b2.members.values_list('id', flat=True))
            for id in query:
                keys.add(id)
            # Usar expressão regular para selecionar as chaves desejadas
            chaves_selecionadas = [chave for chave in chaves if re.match(r'form-\d+-members', chave)]
            for value in chaves_selecionadas:
                value = int(request.POST.get(value,''))
                if value not in keys:
                    # Logica para gravar
                    keys.add(value)
                    b2.members.add(User.objects.get(pk=value))

            # Save stakeholders
            keys = set()
            query = list(b2.stakeholders.values_list('id', flat=True))
            for id in query:
                keys.add(id)
            # Usar expressão regular para selecionar as chaves desejadas
            chaves_selecionadas = [chave for chave in chaves if re.match(r'form-\d+-stakeholders', chave)]
            for value in chaves_selecionadas:
                value = int(request.POST.get(value,''))
                if value not in keys:
                    # Logica para gravar
                    keys.add(value)
                    b2.stakeholders.add(User.objects.get(pk=value))
            pk = b2.pk
            # Mesmo código que o método details
            project = Project.objects.get(pk=pk) # Mesmo código que o método details
            context = {'project': project, 'register': register} # Mesmo código que o método details
            return render(request, 'projects/details.html', context) # Mesmo código que o método details

    else: # Empty new form
        project_form = ProjectForm(prefix='new')

    context = {'project_form': project_form, 'numproject': numproject}
    return render(request, 'projects/new.html', context)


def edit2(request, pk=None):
    numproject = pk
    if request.method == 'POST':    # Newly filled form
        project_form = ProjectForm(request.POST, prefix='repost')
        
        chaves = request.POST.keys()    # Seleciona todas as chaves de request.POST

        #if project_form.is_valid() and building_formset.is_valid():
        if project_form.is_valid():
            a = project_form.cleaned_data['code']
            b = project_form.cleaned_data['year']
            c = project_form.cleaned_data['name']
            d = project_form.cleaned_data['description']
            e = project_form.cleaned_data['created_at']
            f = project_form.cleaned_data['updated_at']
            g = project_form.cleaned_data['site']
            h = project_form.cleaned_data['project_manager']
            i = project_form.cleaned_data['project_manager_support']
            j = project_form.cleaned_data['interlocutor']
            k = project_form.cleaned_data['remarks']
            l = project_form.cleaned_data['project_status']

            register = a
            # # Verifica se já existe uma entrada com a mesma combinação de 'code' e 'year'
            # while Project.objects.filter(code=a, year=b).exists():
            #     # Existe, tenta o próximo disponível
            #     a += 1
            #     register = a

            # Logica para gravar instância principal
            b2 = Project.objects.filter(pk=pk)
            b2.update(code=a, year=b, name=c, description=d, created_at=e, updated_at=f, project_manager=h, project_manager_support=i, project_status=l, interlocutor=j, remarks=k)
            #b2.save()
            b2 = Project.objects.get(pk=pk)

            # Save buildings
            keys = set()
            query = list(b2.buildings.values_list('id', flat=True))
            for id in query:
                keys.add(id)
            
            # Usar expressão regular para selecionar as chaves desejadas
            chaves_selecionadas = [chave for chave in chaves if re.match(r'form-\d+-building', chave)]
            for value in chaves_selecionadas:
                value = int(request.POST.get(value,''))
                if value not in keys:
                    # Logica para gravar
                    keys.add(value)
                    b2.buildings.add(Building.objects.get(pk=value))
            
            # Save members
            keys = set()
            query = list(b2.members.values_list('id', flat=True))
            for id in query:
                keys.add(id)
            # Usar expressão regular para selecionar as chaves desejadas
            chaves_selecionadas1 = [chave for chave in chaves if re.match(r'form-\d+-members', chave)]
            chaves_selecionadas2 = [chave for chave in chaves if re.match(r'dynamic_selects_members_\d+', chave)]
            chaves_selecionadas = chaves_selecionadas1 + chaves_selecionadas2
            for value in chaves_selecionadas:
                value = int(request.POST.get(value,''))
                if value not in keys:
                    # Logica para gravar
                    keys.add(value)
                    b2.members.add(User.objects.get(pk=value))

            # Save stakeholders
            keys = set()
            query = list(b2.stakeholders.values_list('id', flat=True))
            for id in query:
                keys.add(id)
                
            # Usar expressão regular para selecionar as chaves desejadas
            chaves_selecionadas1 = [chave for chave in chaves if re.match(r'form-\d+-stakeholders', chave)]
            chaves_selecionadas2 = [chave for chave in chaves if re.match(r'dynamic_selects_stakeholders_\d+', chave)]
            chaves_selecionadas = chaves_selecionadas1 + chaves_selecionadas2
            
            for value in chaves_selecionadas:
                value = int(request.POST.get(value,''))
                if value not in keys:
                    # Logica para gravar
                    keys.add(value)
                    b2.stakeholders.add(User.objects.get(pk=value))
            pk = b2.pk

            # Mesmo código que o método details
            project = Project.objects.get(pk=pk) # Mesmo código que o método details
            context = {'project': project, 'register': register} # Mesmo código que o método details
            return render(request, 'projects/details.html', context) # Mesmo código que o método details

    else:
        instance = Project.objects.get(pk=numproject)
        project_form = ProjectForm(instance=instance, prefix='edit')
    
    project_profile = Project.objects.get(pk=numproject)
    #project_form = ProjectForm(instance=project_profile, pk=numproject)
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
    return render(request, 'projects/edit.html', context)

# 
# def edit(request, pk=None):
#     numproject = pk
#     extra_forms = 1  # You can set the initial number of forms here
#     #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)

#     if request.method == 'POST':
#         project_form = ProjectForm2(request.POST, pk=pk)
#         project_form.fields['site'].widget.attrs['disabled'] = True
#         #if project_form.is_valid() and building_formset.is_valid():

#         # Consulta para obter os prédios que pertencem ao site e não estão associados ao projeto
#         # Evita inserção de dados repetidos
#         project_profile = Project.objects.get(pk=numproject)
#         siteID = project_profile.buildings.first().site.id
#         buildings_query = Building.objects.filter(site_id=siteID)
#         inner_queryset = Project.objects.filter(Q(id=pk)&Q(buildings__site=siteID))
#         results = buildings_query.exclude(buildings__id__in=inner_queryset).values_list('id', flat=True)

#         # Execute a consulta
#         #queryset = results.distinct()
#         buildings_queryset = list(results.distinct())

#         # Consulta para obter os usuários que pertencem ao projeto
#         # Evita inserção de dados repetidos
#         members_query = list(User.objects.filter(members=pk).values_list('id', flat=True))

#         # Consulta para obter os stakeholders que pertencem ao projeto
#         # Evita inserção de dados repetidos
#         stakeholders_query = list(User.objects.filter(stakeholders=pk).values_list('id', flat=True))

#         if project_form.is_valid():
#             a = project_form.cleaned_data['name']
#             b = project_form.cleaned_data['description']
#             c = project_form.cleaned_data['created_at']
#             d = project_form.cleaned_data['updated_at']
#             e = project_form.cleaned_data['site']

#             # Logica para gravar instância principal
#             b2 = Project.objects.filter(pk=pk)
#             b2.update(name=a, description=b, updated_at=d)
#             b2 = Project.objects.get(pk=pk)

#             # Save Buildings
#             counter = 0
#             keys = set()
#             #while (value := request.POST.get('form-'+str(counter)+'building', '')) != '':
#             for value in buildings_queryset:
#                 if value not in keys:
#                     # Logica para gravar
#                     keys.add(value)
#                     b2.buildings.add(Building.objects.get(pk=value))
#                 counter += 1

#             # Save members
#             keys = set()
#             # Define o padrão que as chaves devem seguir
#             padrao = re.compile(r'form-\d+-members')

#             # Seleciona as chaves que correspondem ao padrão    
#             chaves_selecionadas = [chave for chave in request.POST.keys() if padrao.match(chave)]

#             while chaves_selecionadas:
#                 value = int(request.POST[chaves_selecionadas.pop()])
#                 if value not in keys and value not in members_query:
#                     # Logica para gravar
#                     keys.add(value)
#                     b2.members.add(User.objects.get(pk=value))

#             # Save stakeholders
#             keys = set()
#             # Define o padrão que as chaves devem seguir
#             padrao = re.compile(r'form-\d+-stakeholders')

#             # Seleciona as chaves que correspondem ao padrão    
#             chaves_selecionadas = [chave for chave in request.POST.keys() if padrao.match(chave)]

#             while chaves_selecionadas:
#                 value = int(request.POST[chaves_selecionadas.pop()])
#                 if value not in keys and value not in stakeholders_query:
#                     # Logica para gravar
#                     keys.add(value)
#                     b2.stakeholders.add(User.objects.get(pk=value))

#     project_profile = Project.objects.get(pk=numproject)
#     #members = project_profile.members.all()
#     #stackholders = project_profile.members.all()
#     project_form = ProjectForm2(instance=project_profile, pk=numproject)
#     members_formset = set_MembersFormSet(project_profile)
#     stakeholders_formset = set_stakeholders_formset(project_profile)
    
#     # Make selectbox
#     siteID = project_profile.buildings.first().site.id 
#     buildings_formset = set_buildings_formset(project_profile)
#     criterion1 = Q(site_id=siteID)
#     queryset = Building.objects.filter(criterion1)
#     for form in buildings_formset.forms:
#         form.fields['building'].queryset = queryset

#     context = {'project_form': project_form,
#                'numproject': numproject,
#                'members_formset': members_formset,
#                'stakeholders_formset': stakeholders_formset,
#                'buildings_formset': buildings_formset,
#                }
#     return render(request, 'projects/edit.html', context)
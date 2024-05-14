from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required



from django.db import IntegrityError
from django.contrib import messages

from django.http import HttpResponse
from django.views.generic import View

from django.db.models import Q

import re

from makemake.core.custom_functions import separar_valores_sem_espaco, is_list_empty


from makemake.agreements.models import Agreement
from makemake.projects.models import Project
from makemake.agreements.forms import AgreementForm



def void(request):
    return HttpResponseRedirect('')


def home(request, pk=None):
    instance = Project.objects.get(pk=pk)
    items = Agreement.objects.filter(project=instance).order_by('start')
    return render(request, 'agreements/home.html', {'items': items, 'instance': instance})

# 
# def home2(request, pk=None):
#     instance = Project.objects.get(pk=pk)
#     items = Agreement.objects.filter(project=instance).order_by('start')
#     return render(request, 'agreements/home2.html', {'items': items, 'instance': instance})


def delete(request, pk):
    if request.user.has_perm('global_permissions.entra_em_agreements'):
        numproject = Agreement.objects.get(pk=pk).project.id
        try:
            register_to_delete = get_object_or_404(Agreement, pk=pk)
            register_to_delete.delete()
        except IntegrityError:
            message = "The register couldn't be deleted!"
            messages.info(request, message)
    else:
        message = "You cannot have permission to do this!"
        messages.info(request, message)
    return home(request, numproject)



def search(request):
    # Expressão regular
    # String de exemplo
    #string = "   123   /   456  "

    regex = r"^\s*(\d+)\s*\/\s*(\d+)\s*$"

    # Texto de consulta enviado através do formulário
    input_text = request.GET.get('search', None)

    if input_text == '' or input_text is None:
        items = Agreement.objects.all().order_by('start')
        return render(request, 'agreements/home.html', {'items': items})

    # Verifica se a string corresponde ao padrão
    match = re.match(regex, input_text)

    if match: # Check if pattern is code / year
        x = int(match.group(1))  # Captura o valor de X
        y = int(match.group(2))  # Captura o valor de Y
        # Use Q objects para filtrar seu modelo
        items = Agreement.objects.filter(Q(description=x) & Q(description=y)).order_by('start')
    else:   # Pattern is a free string
        and_list, or_list = separar_valores_sem_espaco(input_text)
        if is_list_empty(and_list) and is_list_empty(or_list):
            items = Agreement.objects.filter(Q(description__icontains=input_text)).order_by('start')
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
            if not is_list_empty(and_list) and  is_list_empty(or_list):
                final_string = string_and
            elif is_list_empty(and_list) and  not is_list_empty(or_list):
                final_string = string_or
            items = Agreement.objects.filter(eval(final_string)).order_by('start')
    return render(request, 'agreements/home.html', {'items': items})


def void(View):
    def dispatch(self, request, *args, **kwargs):
            # Coloque aqui sua lógica que não retorna nada para o template
            # Por exemplo, processamento de dados, atualizações no banco de dados, etc.
            
            # Após executar a lógica, você pode simplesmente retornar uma resposta vazia
            return HttpResponse(status=204)  # 204 significa "No Content"


def new(request, numproject=None):
    if not request.user.has_perm('global_permissions.entra_em_aggrements'):
        message = "You cannot have permission to do this!"
        messages.info(request, message)
        return home(request)

    if request.method == 'POST':    # Newly filled form
        form = AgreementForm(request.POST or None, numproject=numproject, prefix='repost')

        if form.is_valid():
            a = form.cleaned_data['description']
            b = form.cleaned_data['category']
            c = form.cleaned_data['start']
            d = form.cleaned_data['end']
            e = form.cleaned_data['project']

            # Logica para gravar instância principal
            instance = Project.objects.get(pk=e)
            b2 = Agreement(description=a, category=b, start=c, end=d, project=instance)
            try:
                b2.save()
                items = Agreement.objects.filter(project=instance).order_by('start')
                return render(request, 'agreements/home.html', {'items': items, 'instance': instance})
            except IntegrityError as e:
                #messages.add_message(request, messages.ERROR, 'There has been an error...')
                form.add_error('code', 'Code category must be unique!')
                #context = {'form': form}
                #return render(request, 'categories/new.html', context)

    else: # Empty new form
        form = AgreementForm(numproject=numproject, prefix='new')

    context = {'form': form, 'numproject': numproject}
    return render(request, 'agreements/new_or_edit.html', context)


def edit(request, pk=None):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)
    if request.user.has_perm('global_permissions.entra_em_agreements'):

        if request.method == 'POST':    # Newly filled form
            form = AgreementForm(request.POST or None)

            if form.is_valid():
                a = form.cleaned_data['description']
                b = form.cleaned_data['category']
                c = form.cleaned_data['start']
                d = form.cleaned_data['end']

                # Logica para gravar instância principal
                b2 = Agreement.objects.filter(pk=pk)
                b2.update(description=a, category=b, start=c, end=d)

        else: # Read data from 
            instance = Agreement.objects.get(pk=pk)
            form = AgreementForm(instance=instance, prefix='edit')
        # context = {'form': form}
        # return render(request, 'agreements/new_or_edit.html', context)
        context = {'form': form, 'numproject': instance.project_id}
        return render(request, 'agreements/new_or_edit.html', context)
    message = "You cannot have permission to do this!"
    messages.info(request, message)
    projectid=Agreement.objects.get(pk=pk).project.id
    return home(request, pk=projectid)


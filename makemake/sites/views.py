from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.contrib import messages

from django.http import HttpResponse
from django.views.generic import View

from django.db.models import Q

from makemake.sites.models import Site
from makemake.sites.forms import SiteForm
from makemake.core.custom_functions import update_object

from auditlog.context import set_actor

import re

from makemake.core.custom_functions import separar_valores_sem_espaco, is_list_empty


def delete(request, pk):
    if request.user.has_perm('global_permissions.entra_em_sites'):
        project = Site.objects.get(pk=pk)
        try:
            register_to_delete = get_object_or_404(Site, pk=pk)
            register_to_delete.delete()
        except IntegrityError:
            message = "The register couldn't be deleted!"
            messages.info(request, message)
    else:
        message = "You cannot have permission to do this!"
        messages.info(request, message)
    return home(request)
    

def home(request):
    items = Site.objects.all()
    messages.info(request, None)
    return render(request, 'sites/home.html', {'items': items})



def search(request):
    # Expressão regular
    # String de exemplo
    #string = "   123   /   456  "

    regex = r"^\s*(\d+)\s*\/\s*(\d+)\s*$"

    # Texto de consulta enviado através do formulário
    input_text = request.GET.get('search', None)

    if input_text == '' or input_text is None:
        items = Site.objects.all().order_by('name')
        return render(request, 'sites/home.html', {'items': items})

    # Verifica se a string corresponde ao padrão
    match = re.match(regex, input_text)

    if match: # Check if pattern is code / year
        x = int(match.group(1))  # Captura o valor de X
        y = int(match.group(2))  # Captura o valor de Y
        # Use Q objects para filtrar seu modelo
        items = Site.objects.filter(Q(name=x) & Q(name=y)).order_by('name')
    else:   # Pattern is a free string
        and_list, or_list = separar_valores_sem_espaco(input_text)
        if is_list_empty(and_list) and is_list_empty(or_list):
            items = Site.objects.filter(Q(name__icontains=input_text)).order_by('name')
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
            items = Site.objects.filter(eval(final_string)).order_by('name')
    return render(request, 'sites/home.html', {'items': items})


def void(View):
    def dispatch(self, request, *args, **kwargs):
            # Coloque aqui sua lógica que não retorna nada para o template
            # Por exemplo, processamento de dados, atualizações no banco de dados, etc.
            
            # Após executar a lógica, você pode simplesmente retornar uma resposta vazia
            return HttpResponse(status=204)  # 204 significa "No Content"


def new(request):
    if not request.user.has_perm('global_permissions.entra_em_sites'):
        message = "You cannot have permission to do this!"
        messages.info(request, message)
        return home(request)

    if request.method == 'POST':    # Newly filled form
        form = SiteForm(request.POST or None)

        if form.is_valid():
            a = form.cleaned_data['name']
            b = form.cleaned_data['place']

            # Logica para gravar instância principal
            b2 = Site(name=a, place=b, )
            try:
                with set_actor(request.user):
                    b2.save()
            except IntegrityError as e:
                #messages.add_message(request, messages.ERROR, 'There has been an error...')
                form.add_error('code', 'Code category must be unique!')
                #context = {'form': form}
                #return render(request, 'categories/new.html', context)

    else: # Empty new form
        form = SiteForm()

    context = {'form': form}
    return render(request, 'sites/new_or_edit.html', context)



def edit(request, pk=None):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)
    if request.user.has_perm('global_permissions.entra_em_sites'):

        if request.method == 'POST':    # Newly filled form
            form = SiteForm(request.POST or None)

            if form.is_valid():
                a = form.cleaned_data['name']
                b = form.cleaned_data['place']
                # Lista de atributos do modelo Project
                attributes = [
                    "name", "place", 
                ]
                # Lista de valores correspondentes
                values = [a, b,]
                update_object(request, Site, pk, attributes, values)

        else: # Read data from 
            instance = Site.objects.get(pk=pk)
            form = SiteForm(instance=instance, prefix='edit')
        context = {'form': form}
        return render(request, 'sites/new_or_edit.html', context)
    message = "You cannot have permission to do this!"
    messages.info(request, message)
    return home(request)


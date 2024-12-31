from django.shortcuts import get_object_or_404, render
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from makemake.buildings.models import Building
from makemake.buildings.forms import BuildingForm

from makemake.core.custom_functions import separar_valores_sem_espaco, is_list_empty

import re


def home(request):
    items = Building.objects.all().order_by('number')
    return render(request, 'buildings/home.html', {'items': items})


def delete(request, pk):
    project = Building.objects.get(pk=pk)
    try:
        register_to_delete = get_object_or_404(Building, pk=pk)
        register_to_delete.delete()
    except IntegrityError:
        message = "The register couldn't be deleted!"
        messages.info(request, message)
    return home(request)


def search(request):
    # Expressão regular
    # String de exemplo
    #string = "   123   /   456  "

    regex = r"^\s*(\d+)\s*\/\s*(\d+)\s*$"

    # Texto de consulta enviado através do formulário
    input_text = request.GET.get('search', None)

    if input_text == '' or input_text is None:
        items = Building.objects.all().order_by('number', 'name')
        return render(request, 'buildings/home.html', {'items': items})

    # Verifica se a string corresponde ao padrão
    match = re.match(regex, input_text)

    if match: # Check if pattern is code / year
        x = int(match.group(1))  # Captura o valor de X
        y = int(match.group(2))  # Captura o valor de Y
        
        # Usa Q objects para filtrar o modelo
        items = Building.objects.filter(Q(name=x) & Q(name=y)).order_by('number', 'name')
    else:   # Pattern is a free string
        and_list, or_list = separar_valores_sem_espaco(input_text)
        if is_list_empty(and_list) and is_list_empty(or_list):
            items = Building.objects.filter(Q(name__icontains=input_text)).order_by('number', 'name')
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
            items = Building.objects.filter(eval(final_string)).order_by('number', 'name')
    return render(request, 'buildings/home.html', {'items': items})


def new(request):

    if request.method == 'POST':    # Newly filled form
        form = BuildingForm(request.POST or None)

        if form.is_valid():
            a = form.cleaned_data['name']
            b = form.cleaned_data['number']
            c = form.cleaned_data['site']
            d = form.cleaned_data['status']
            e = form.cleaned_data['created_at']
            f = form.cleaned_data['updated_at']

            # Logica para gravar instância principal
            b2 = Building(name=a, number=b, site=c, status=d, created_at=e, updated_at=f, )

            try:
                b2.save()
            except IntegrityError as e:
                form.add_error('number', 'Building number must be unique!')

    else: # Empty new form
        form = BuildingForm(prefix='new')

    context = {'form': form}
    return render(request, 'buildings/new_or_edit.html', context)


def edit(request, pk=None):

    if request.method == 'POST':    # Newly filled form
        form = BuildingForm(request.POST or None)

        if form.is_valid():
            a = form.cleaned_data['name']
            b = form.cleaned_data['number']
            c = form.cleaned_data['site']
            d = form.cleaned_data['status']
            e = form.cleaned_data['created_at']
            f = form.cleaned_data['updated_at']

            # Logica para gravar instância principal
            b2 = Building.objects.filter(pk=pk)
            b2.update(name=a, status=d, updated_at=f, )
            items = Building.objects.all().order_by('number')
            return render(request, 'buildings/home.html', {'items': items})
            # # Logica para gravar instância principal
            # try:
            #     b2.save()
            # except IntegrityError as e:
            #     #messages.add_message(request, messages.ERROR, 'There has been an error...')
            #     form.add_error('code', 'Code Building must be unique!')
            #     #context = {'form': form}
            #     #return render(request, 'categories/new.html', context)

    else: # Read data from 
        instance = Building.objects.get(pk=pk)
        form = BuildingForm(instance=instance, prefix='edit')

    context = {'form': form}
    return render(request, 'buildings/new_or_edit.html', context)

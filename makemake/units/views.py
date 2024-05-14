from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import IntegrityError
from django.contrib import messages

from makemake.units.models import Unit
from makemake.units.forms import UnitForm

from makemake.core.custom_functions import separar_valores_sem_espaco, is_list_empty

import re


def search(request):
    # Expressão regular
    # String de exemplo
    #string = "   123   /   456  "

    regex = r"^\s*(\d+)\s*\/\s*(\d+)\s*$"

    # Texto de consulta enviado através do formulário
    input_text = request.GET.get('search', None)

    if input_text == '' or input_text is None:
        items = Unit.objects.all()
        return render(request, 'units/home.html', {'items': items})

    # Verifica se a string corresponde ao padrão
    match = re.match(regex, input_text)

    if match: # Check if pattern is code / year
        x = int(match.group(1))  # Captura o valor de X
        y = int(match.group(2))  # Captura o valor de Y
        # Usa Q objects para filtrar o modelo
        items = Unit.objects.filter(Q(code=x) & Q(name=y)).order_by('name')
    else:   # Pattern is a free string
        and_list, or_list = separar_valores_sem_espaco(input_text)
        if is_list_empty(and_list) and is_list_empty(or_list):
            items = Unit.objects.filter(Q(name__icontains=input_text)).order_by('name')
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
            items = Unit.objects.filter(eval(final_string)).order_by('name')
    return render(request, 'units/home.html', {'items': items})


def delete(request, pk):
    #instance = Unit.objects.get(pk=pk)
    try:
        register_to_delete = get_object_or_404(Unit, pk=pk)
        register_to_delete.delete()
    except IntegrityError:
        message = "The register couldn't be deleted!"
        messages.info(request, message)
    return home(request)
    

def home(request):
    items = Unit.objects.all().order_by('name',)
    return render(request, 'units/home.html', {'items': items})


def new(request):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)

    if request.method == 'POST':    # Newly filled form
        form = UnitForm(request.POST or None)

        if form.is_valid():
            a = form.cleaned_data['name']
            b = form.cleaned_data['symbol']
            c = form.cleaned_data['type']
            d = form.cleaned_data['symbol_alternative1']
            e = form.cleaned_data['symbol_alternative2']

            
            a = a.lower().capitalize()

            # Logica para gravar instância principal
            b2 = Unit(name=a, symbol=b, type=c, )
            try:
                b2.save()
                form = UnitForm()
            except IntegrityError as e:
                #messages.add_message(request, messages.ERROR, 'There has been an error...')
                form.add_error('code', 'Code category must be unique!')
                #context = {'form': form}
                #return render(request, 'categories/new.html', context)

    else: # Empty new form
        form = UnitForm()

    context = {'form': form}
    return render(request, 'units/new_or_edit.html', context)


def edit(request, pk=None):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)

    if request.method == 'POST':    # Newly filled form
        form = UnitForm(request.POST or None)

        if form.is_valid():
            a = form.cleaned_data['name']
            b = form.cleaned_data['symbol']
            c = form.cleaned_data['type']
            d = form.cleaned_data['symbol_alternative1']
            e = form.cleaned_data['symbol_alternative2']
            
            a = a.lower().capitalize()

            # Logica para gravar instância principal
            b2 = Unit.objects.filter(pk=pk)
            b2.update(name=a, symbol=b, type=c, symbol_alternative1=d, symbol_alternative2=e)
            # # Logica para gravar instância principal
            # try:
            #     b2.save()
            # except IntegrityError as e:
            #     #messages.add_message(request, messages.ERROR, 'There has been an error...')
            #     form.add_error('code', 'Code category must be unique!')
            #     #context = {'form': form}
            #     #return render(request, 'categories/new.html', context)

    else: # Read data from 
        instance = Unit.objects.get(pk=pk)
        form = UnitForm(instance=instance, prefix='edit')

    context = {'form': form}
    return render(request, 'units/new_or_edit.html', context)


def details(request, pk):
    instance = Unit.objects.get(pk=pk)
    context = {'category': instance, }
    return render(request, 'units/details.html', context)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.db import IntegrityError
from django.utils.text import slugify

from makemake.categories.models import Category
from makemake.categories.forms import CategoryForm, CategoryFormSet, ParentsForm

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
        items = Category.objects.all()
        return render(request, 'categories/home.html', {'items': items})

    # Verifica se a string corresponde ao padrão
    match = re.match(regex, input_text)

    if match: # Check if pattern is code / year
        x = int(match.group(1))  # Captura o valor de X
        y = int(match.group(2))  # Captura o valor de Y
        # Usa Q objects para filtrar o modelo
        items = Category.objects.filter(Q(code=x) & Q(name=y)).order_by('code', 'name')
    else:   # Pattern is a free string
        and_list, or_list = separar_valores_sem_espaco(input_text)
        if is_list_empty(and_list) and is_list_empty(or_list):
            items = Category.objects.filter(Q(name__icontains=input_text)).order_by('code', 'name')
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
            items = Category.objects.filter(eval(final_string)).order_by('code', 'name')
    return render(request, 'categories/home.html', {'items': items})


def delete(request, pk):
    project = Category.objects.get(pk=pk)
    try:
        register_to_delete = get_object_or_404(Category, pk=pk)
        register_to_delete.delete()
    except IntegrityError:
        message = "The register couldn't be deleted!"
        messages.info(request, message)
    return home(request)
    

def home(request):
    
    items = Category.objects.annotate(parent_count=Count('parents')).order_by('parent_count', 'code', 'name', )
    return render(request, 'categories/home.html', {'items': items})

def add_or_edit(request, pk=None):
    category = Category.objects.filter(pk=pk)
    check_exists = category.exists()

    if request.method == 'POST':
        if check_exists:   ################################# EDIT
            form = CategoryForm(request.POST or None)
            formset = CategoryFormSet(request.POST or None)

            if form.is_valid():
                a = form.cleaned_data['code'].upper()
                b = form.cleaned_data['name']
                c = form.cleaned_data['description']
                e = form.cleaned_data['fordocs']
                f = form.cleaned_data['forbudgets']

                chaves = request.POST.keys()    # Seleciona todas as chaves de request.POST

                # Logica para gravar instância principal
                b2 = Category.objects.filter(pk=pk)
               
                try:
                    # Usar expressão regular para selecionar as chaves desejadas
                    selected_keys = [chave for chave in chaves if re.match(r'form-INPUT-(\d+)', chave)]
                    values_list = []

                    for key in selected_keys:
                        value = request.POST.get(key,'')
                        if value != '':
                            values_list.append(value)
                    set_one = set(values_list)

                    # Build second list of elements , build from database
                    instance = b2.first()
                    categories = instance.parents.all().values('id',)
                    set_two = {str(value['id']) for value in categories}

                    # elementos que estão em list_two, mas não estão em list_one
                    components_deleted = list(set_two.difference(set_one))

                    # elementos que estão em ambas os conjuntos
                    components_in_both = list(set_one.intersection(set_two))

                    # elementos que estão em list_two, mas não estão em list_one
                    components_added = list(set_one.difference(set_two))

                    categories_to_add = [Category.objects.get(pk=value) for value in components_added]
    
                    # Update instance
                    b2.update(name=b, description=c, fordocs=e, forbudgets=f)

                    # Delete components
                    category1 = b2.first()

                    for key in components_deleted:
                        category2 = Category.objects.get(pk=key)
                        category1.parents.remove(category2)
                    
                    for instance in categories_to_add:
                        category1.parents.add(instance)

                    form = CategoryForm()
                    formset = CategoryFormSet()
                except IntegrityError as e:
                    form.add_error('code', 'Code category must be unique!')

        else:  ###################################### NEW
            form = CategoryForm(request.POST or None)
            formset = CategoryFormSet(request.POST or None)


            if form.is_valid() and formset.is_valid():
                a = form.cleaned_data['code']
                b = form.cleaned_data['name']
                c = form.cleaned_data['description']
                e = form.cleaned_data['fordocs']
                f = form.cleaned_data['forbudgets']
                
                chaves = request.POST.keys()    # Seleciona todas as chaves de request.POST

                b = b.upper() if len(formset) is None else b.lower().capitalize()

                # Logica para gravar instância principal
                b2 = Category(code=a, name=b, description=c, fordocs=e, forbudgets=f)
                try:
                    # Usar expressão regular para selecionar as chaves desejadas
                    selected_keys = [chave for chave in chaves if re.match(r'form-INPUT-(\d+)', chave)]
                    values_list = []
    
                    for key in selected_keys:
                        parentID = request.POST.get(key, '')  # Get the component ID
                        if parentID is not '':
                            b3 = Category.objects.get(pk=parentID)
                            values_list.append(b3)

                    b2.save()
                    new_obj = Category.objects.get(id=b2.id)
                    
                    for instance in values_list:
                        new_obj.parents.add(instance)

                    form = CategoryForm()
                    formset = CategoryFormSet()
                except IntegrityError as e:
                    form.add_error('code', 'Code category must be unique!')
    else:   ######################################## GET
        if check_exists:    ######################## EDIT
            # Obtendo a categoria com suas categorias relacionadas (pais)
            instance = Category.objects.prefetch_related('parents').get(pk=pk)
            form = CategoryForm(instance=instance, prefix='edit')

            # Get parents from instance
            related_parents = instance.parents.all()

            # Adiciona os valores iniciais aos fields

            # Inicializar o formset com os pais relacionados
            formset = CategoryFormSet(initial=[{'parent': parent.id} for parent in related_parents])

        else:   ################################### NEW
            form = CategoryForm()
            formset = CategoryFormSet()

    context = {
        'form': form,
        'formset': formset,}
    return render(request, 'categories/new_or_edit.html', context)

def details(request, pk):
    category = Category.objects.get(pk=pk)
    context = {'category': category, }
    return render(request, 'categories/details.html', context)
import re
from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.db.models import Max, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

from makemake.prices.models import Price, PriceLabel
from makemake.compositions.models import Composition, CompositionHasComponents

from makemake.compositions.forms import CompositionForm, ComponentForm, CompositionPriceFormSet

from makemake.core.choices import ORIGIN_PRICES_CHOICES, BUDGETS_DATABASES_CHOICES, PLACES_CHOICES
#from makemake.sites.models import Site
#from makemake.buildings.models import Building
#from makemake.buildings.forms import BuildingForm, SelectBuildingForm
# from makemake.projects.forms import ProjectForm, ProjectBuildingForm, ProjectForm2, ProjectForm3
#from makemake.projects.forms import ProjectForm, ProjectBuildingForm
#from makemake.projects.models import Project
#from makemake.documents.models import Document

#from makemake.projects.forms import UserForm, MembersForm, set_MembersFormSet, set_stakeholders_formset, set_buildings_formset

from makemake.core.custom_functions import is_list_empty, separar_valores_com_espaco, separar_valores_sem_espaco


ITEMS_PER_PAGE_COMPOSITIONS = 40

@permission_required('makemake.can_delete_mymodel')
def delete_mymodel(request, pk):
    mymodel = get_object_or_404(Composition, pk=pk)
    if mymodel.can_be_deleted():
        mymodel.delete()
        return redirect('mymodel_list')
    else:
        raise PermissionDenied

@permission_required('makemake.can_change_mymodel')
def change_mymodel(request, pk):
    mymodel = get_object_or_404(Composition, pk=pk)
    if mymodel.can_be_changed():
        # lógica para alterar o registro
        pass
    else:
        raise PermissionDenied



# Modify search

def search2(request):
    # Regex para detectar número / numero ou seja code / year
    regex = r"^\s*(\d+)\s*\/\s*(\d+)\s*$" 
    # Regex para detectar apenas números sem espaços entre grupos ou seja um único numero
    regex2 = r"^\s*(\d+)\s*$"  
    # Regex para capturar números ou palavras separadas por espaços
    regex3 = r"^\s*(\d+|[a-zA-Z]+(?:\s+[a-zA-Z]+)*)\s*$"
    input_text = request.GET.get('search', None)

    if input_text == '' or input_text is None:
        items = Composition.objects.all()
    else:
        match = re.match(regex2, input_text)
        if match:
            x = int(match.group(1))
            items = Composition.objects.filter(Q(code=x))
        else:
            and_list, or_list = separar_valores_sem_espaco(input_text)
            if is_list_empty(and_list) and is_list_empty(or_list):
                items = Composition.objects.filter(Q(description__icontains=input_text))
            else:
                string_and = ''
                string_or = ''
                pattern = 'Q(description__icontains='
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
                items = Composition.objects.filter(eval(final_string))

    # Paginação dos resultados
    paginator = Paginator(items, ITEMS_PER_PAGE_COMPOSITIONS)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'compositions/home.html', {'items': items, 'search_text': input_text})

# ORIGINAL SEARCH

def search(request):
    # Expressão regular
    # String de exemplo
    #string = "   123   /   456  "

    regex = r"^\s*(\d+)\s*\/\s*(\d+)\s*$"

    # Texto de consulta enviado através do formulário
    input_text = request.GET.get('search', None)

    if input_text == '' or input_text is None:
        items = Composition.objects.all()
        items = paginacao(request, items, ITEMS_PER_PAGE_COMPOSITIONS)
        return render(request, 'compositions/home.html', {'items': items})

    # Verifica se a string corresponde ao padrão
    match = re.match(regex, input_text)

    if match: # Check if pattern is code / year
        x = int(match.group(1))  # Captura o valor de X
        y = int(match.group(2))  # Captura o valor de Y
        # Use Q objects para filtrar seu modelo
        items = Composition.objects.filter(Q(code=x) & Q(year=y))
    else:   # Pattern is a free string
        and_list, or_list = separar_valores_sem_espaco(input_text)
        if is_list_empty(and_list) and is_list_empty(or_list):
            items = Composition.objects.filter(Q(description__icontains=input_text))
        else:
            ### FUNCAO ABAIXO NÃO ESTA FUNCIONANDO
            ### PRECISA REFATORAR PARA FICAR MUITO MELHOR
            string_and = ''
            string_or = ''
            pattern = 'Q(description__icontains='
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
            items = Composition.objects.filter(eval(final_string))
        items = paginacao(request, items, ITEMS_PER_PAGE_COMPOSITIONS)
    return render(request, 'compositions/home.html', {'items': items})


def paginacao(request, items, items_per_page=25):
    paginator = Paginator(items, items_per_page)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um número inteiro, retorna a primeira página
        items = paginator.page(1)
    except EmptyPage:
        # Se a página está fora do intervalo (e.g. 9999), retorna a última página de resultados
        items = paginator.page(paginator.num_pages)
    return items


def search_components(request):
    # Regex para detectar número / numero ou seja code / year
    regex = r"^\s*(\d+)\s*\/\s*(\d+)\s*$" 
    # Regex para detectar apenas números sem espaços entre grupos ou seja um único numero
    regex2 = r"^\s*(\d+)\s*$"  
    # Regex para capturar números ou palavras separadas por espaços
    regex3 = r"^\s*(\d+|[a-zA-Z]+(?:\s+[a-zA-Z]+)*)\s*$"

    input_text = request.GET.get('q', '')
    and_list, or_list = separar_valores_sem_espaco(input_text)
    if is_list_empty(and_list) and is_list_empty(or_list):
        input_text = input_text.strip()
        final_string = 'Q(description__icontains=' + input_text + ')'
        #items = Composition.objects.filter(Q(description__icontains=input_text)).values('id', 'description', 'dbtype')
        #results = items
        #results = [{'value': result['id'], 'text': result['description'], 'dbtype': result['dbtype']} for result in results]
        #return JsonResponse(results, safe=False)
    elif len(and_list) == 1 and is_list_empty(or_list) and re.match(regex2, input_text):
        input_text = input_text.strip()
        final_string = 'Q(code=' + input_text + ')'
        #items = Composition.objects.filter(code=input_text).values('id', 'description', 'dbtype')
        #results = items
        #results = [{'value': result['id'], 'text': result['description'], 'dbtype': result['dbtype']} for result in results]
        #return JsonResponse(results, safe=False)
    else:
        string_and = ''
        string_or = ''
        pattern = 'Q(description__icontains='
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
    query = final_string
    if query:
        results = Composition.objects.filter(eval(final_string)).values('id', 'code', 'dbtype', 'description', 'iscomposition', 'unit__symbol')
        results = [{'id': result['id'],
                    'description': result['description'],
                    'code': result['code'],
                    'dbtype': result['dbtype'],
                    'iscomposition': result['iscomposition'],
                    'unit': result['unit__symbol'],
                    } for result in results]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


def delete(request, pk):
    instance = Composition.objects.get(pk=pk)
    #condition1 = len(has_linked_documents(project))
    #if condition1:
    #    return JsonResponse({'success': False})
    
    # Apply a filter to select only those components that have a matching composition_master_id
    components = CompositionHasComponents.objects.filter(
        composition_master_id=instance.pk
    ).order_by(
        'composition_slave__dbtype',
        '-composition_slave__iscomposition',
        'composition_slave__code'
    ).values_list('composition_slave__id', flat=True)
    
    # Delete components from composition
    CompositionHasComponents.objects.filter(composition_slave__id__in=components).delete()
    # Delete composition instance
    instance.delete()

    # Add (an optional) success message
    messages.success(request, "Componentes excluídos com sucesso.")

    return home(request)

# 
# def has_linked_documents(value):
#     return Document.objects.select_related('project').filter(project=value)


def duplicate(request, pk):
    # Get composition
    instance = Composition.objects.get(pk=pk)

    # Get the related CompositionHasComponents instances
    components = CompositionHasComponents.objects.filter(composition_master__id=pk).order_by('composition_slave__dbtype', '-composition_slave__iscomposition', 'composition_slave__code')

    db_default = BUDGETS_DATABASES_CHOICES[1][0]  # OWN database selected
    
    # Get Composition instance with max code
    max_code = Composition.objects.annotate(
        code_as_int=Cast('code', IntegerField())).filter(~Q(code_as_int=None)
                                                         and Q(dbtype=db_default)).aggregate(
                                                             max_code_as_int=Max('code_as_int'))['max_code_as_int'] + 1
    
    # Logica para gravar 
    b1 = Composition(code=max_code, description="DUPLICATE - " + instance.description,
                     unit=instance.unit, type=instance.type, iscomposition=instance.iscomposition,
                     dbtype=db_default, discontinued=instance.discontinued,)
    values_list = CompositionHasComponents.objects.filter(composition_master__id=pk).values_list('composition_slave__id', 'origin', 'quantity')
    try:
        # Save the duplicate register
        b1.save()

        # Which is the master composition
        instance = Composition.objects.get(Q(code=max_code) &
                                              Q(dbtype=db_default)
                                              )
        
        for item in values_list:
            b2 = Composition.objects.get(id=item[0])    # The slave composition (component from composition)
            b3 = CompositionHasComponents(composition_master=instance, composition_slave=b2, origin=item[1], quantity=item[2])
            b3.save()
    except IntegrityError as e:
        messages.error(request, "Error. Message not sent.")

    # Get composition
    instance = Composition.objects.get(pk=instance.id)
    # Get the related CompositionHasComponents instances
    components = CompositionHasComponents.objects.filter(composition_master_id=pk).order_by('composition_slave__dbtype', '-composition_slave__iscomposition', 'composition_slave__code')

    context = {
        'instance': instance,
        'components': components,
    }

    # Format date 
    #instance.created_at = instance.created_at.strftime('%Y-%m-%d')
    #instance.updated_at = instance.updated_at.strftime('%Y-%m-%d')

    #context = {'instance': instance}
    return render(request, 'compositions/details.html', context)



def details(request, pk):
    instance = Composition.objects.get(pk=pk)

    # Get the related CompositionHasComponents instances
    components = CompositionHasComponents.objects.filter(composition_master_id=pk).order_by('composition_slave__dbtype', '-composition_slave__iscomposition', 'composition_slave__code')

    context = {
        'instance': instance,
        'components': components,
    }

    # Format date 
    #instance.created_at = instance.created_at.strftime('%Y-%m-%d')
    #instance.updated_at = instance.updated_at.strftime('%Y-%m-%d')

    #context = {'instance': instance}
    return render(request, 'compositions/details.html', context)


def home(request):
    items = Composition.objects.all()
    items = paginacao(request, items, ITEMS_PER_PAGE_COMPOSITIONS)
    return render(request, 'compositions/home.html', {'items': items})


def new(request):
    if request.method == 'POST':    # Newly filled form
        form = CompositionForm(request.POST or None)

        chaves = request.POST.keys()    # Seleciona todas as chaves de request.POST

        if form.is_valid():
            a = form.cleaned_data['code']
            b = form.cleaned_data['description']
            c = form.cleaned_data['unit']
            d = form.cleaned_data['type']
            e = form.cleaned_data['iscomposition']
            f = form.cleaned_data['dbtype']
            g = form.cleaned_data['discontinued']
            h = form.cleaned_data['created_at']
            i = form.cleaned_data['updated_at']
            
            # Logica para gravar
            b1 = Composition(code=a, description=b, unit=c, type=d, iscomposition=e, dbtype=f, discontinued=g, created_at=h, updated_at=i,)
            try:
                # Usar expressão regular para selecionar as chaves desejadas
                selected_keys = [chave for chave in chaves if re.match(r'(ID|quantity|select-option)-\d+', chave)]
                values_list = []
                
                # Read values from HTML template
                for item in range(0, len(selected_keys), 3):
                    value = selected_keys[item]
                    key = int(request.POST.get(value, ''))  # Get the component ID
                    value = selected_keys[item + 1]
                    origin = int(request.POST.get(value, ''))   # Get the % 
                    value = selected_keys[item + 2]
                    quantity = float(request.POST.get(value, ''))
                    b2 = Composition.objects.get(id=key)    # The slave compositions (component from composition)
                    values_list.append((b2, origin, quantity))
                
                b1.save()

                # Which is the master composition
                instance_id = Composition.objects.get(Q(code=a)&Q(dbtype=f))
                
                for item in values_list:
                    b3 = CompositionHasComponents(composition_master=instance_id, composition_slave=item[0], origin=item[1], quantity=item[2])
                    b3.save()
                
                form = CompositionForm()            
            except IntegrityError as e:
                form.add_error('code', 'Code & DBtype must be unique!')
                form.add_error('dbtype', 'Code & DBtype must be unique!')
    else: # Empty new form
        form = CompositionForm()

    context = {'form': form}
    return render(request, 'compositions/new_or_edit.html', context)


def edit(request, pk=None):
    if request.method == 'POST':    # Newly filled form
        form = CompositionForm(request.POST, prefix='repost')

        # Build first list of elements, build from user input
        keys = request.POST.keys()    # Seleciona todas as chaves de request.POST

        # Usar expressão regular para selecionar as chaves desejadas (code component)
        pattern = re.compile(r'(\b(id|code|origin|quantity|select-option|qty)-\d+|\d+-(id|code|origin|quantity|select-option|qty)\b)')
        selected_keys = [key for key in keys if pattern.match(key)]

        components_dict = {}
        component_tuple = ()
        for index, value in enumerate(selected_keys):
            value = request.POST.get(value,'')
            if not (index % 4):
                id = value
            else:
                component_tuple += (value,)
            if index > 0 and not ((index+1) % 4):
                components_dict[id] = component_tuple
                component_tuple = ()          
        #set_one = {tupla[0] for tupla in components_dict.values()}
        set_one = set(components_dict.keys())

        # Build second list of elements , build from database
        instance = Composition.objects.get(pk=pk)
        components = instance.compositions.all().values('id', 'slave', 'code')
        #set_two = {value['code'] for value in components}
        set_two = {str(value['id']) for value in components}

        # elementos que estão em list_two, mas não estão em list_one
        components_deleted = list(set_two.difference(set_one))

        # elementos que estão em ambas os conjuntos
        components_in_both = list(set_one.intersection(set_two))

        # elementos que estão em list_two, mas não estão em list_one
        components_added = list(set_one.difference(set_two))
        
        #if project_form.is_valid() and building_formset.is_valid():
        if form.is_valid():
            a = form.cleaned_data['code']
            b = form.cleaned_data['description']
            c = form.cleaned_data['unit']
            d = form.cleaned_data['type']
            e = form.cleaned_data['iscomposition']
            f = form.cleaned_data['dbtype']
            g = form.cleaned_data['discontinued']
            h = form.cleaned_data['updated_at']

            # Logica para gravar instância principal
            b2 = Composition.objects.filter(pk=pk)
            b2.update(code=a, description=b, unit=c, type=d, iscomposition=e, dbtype=f, discontinued=g, updated_at=h,)
            #b2.save()

            # Delete components
            CompositionHasComponents.objects.filter(Q(composition_master=pk) & Q(composition_slave__in=components_deleted)).delete()
            
            # Update components
            for component in components_in_both:
                b2 = CompositionHasComponents.objects.filter(Q(composition_master=pk) & Q(composition_slave=component))
                b2.update(origin=components_dict[component][1], quantity=components_dict[component][2])

            # Which is the master composition
            master = Composition.objects.get(pk=pk)

            # Add new components
            for component in components_added:
                slave = Composition.objects.get(pk=component)
                b2 = CompositionHasComponents(composition_master=master, composition_slave=slave, origin=components_dict[component][1], quantity=components_dict[component][2])
                b2.save()

            # Mesmo código que o método details
            instance = Composition.objects.get(pk=pk)

            # Get the related CompositionHasComponents instances
            components = CompositionHasComponents.objects.filter(composition_master_id=pk).order_by('composition_slave__dbtype', '-composition_slave__iscomposition', 'composition_slave__code')

            context = {
                'instance': instance,
                'components': components,
            }

            return render(request, 'compositions/details.html', context)

    else:
        
        instance = Composition.objects.get(pk=pk)

        # Get the related CompositionHasComponents instances
        components = CompositionHasComponents.objects.filter(composition_master_id=pk).order_by('composition_slave__dbtype', '-composition_slave__iscomposition', 'composition_slave__code')

        # Adiciona os valores iniciais aos fields
        forms = [ComponentForm(initial={
            'id': component.composition_slave.id,
            'dbtype': component.composition_slave.dbtype,
            'code': component.composition_slave.code,
            'description': component.composition_slave.description,
            'origin': component.origin,
            'quantity': component.quantity,
        }, prefix=str(i+1000)) for i, component in enumerate(components)]

        # Adiciona o atributo id aos fields
        for index, form in enumerate(forms, start=100000):
            for field_name, field in form.fields.items():
                field_slug = slugify(f"{field_name}-{index}")  # Generate unique slug based on field name and index
                field_slug = field_slug.upper() if 'id-' in field_slug else field_slug
                form.fields[field_name].widget.attrs['id'] = field_slug
                #form.fields[field_name].widget.attrs['name'] = field_slug

        form = CompositionForm(instance=instance, prefix='edit')

        context = {
            'form': form,
            'forms': forms,
        }
    return render(request, 'compositions/new_or_edit.html', context)

def prices(request, pk=None):
    instance_composition = Composition.objects.get(pk=pk)
    instance_prices = Price.objects.filter(composition=instance_composition).order_by('-date', '-label')
    if request.method == 'POST':
        formset = CompositionPriceFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                a = form.cleaned_data['price']
                b = form.cleaned_data['label'].id
                # Evite salvar formulários vazios
                objects = []
                if form.cleaned_data:
                    instance_label = PriceLabel.objects.get(pk=b)
                    instance_user = User.objects.get(pk=request.user.id)
                    valid = Price.objects.filter(Q(composition=instance_composition)&Q(label=instance_label)).exists()
                    if not valid:
                        objects.append(Price(composition=instance_composition,
                                        user=instance_user,
                                        label=instance_label,
                                        price=a,
                                        ))
                    else:
                        form.add_error('label', 'Duplicate reference')
            if objects:
                Price.objects.bulk_create(objects)
                formset = CompositionPriceFormSet()         
    else:
        #initial_data = [{'label': item.label, 'price': item.price} for item in instance_composition.price_set.all()]
        #formset = CompositionPriceFormSet(initial=initial_data)
        formset = CompositionPriceFormSet()
        #formset2 = CompositionPriceFormSetInline()
    grafico = [
    "<script>\n",
    "var chartTwo = document.getElementById('chartTwo');\n",
    "var myLineChart = new Chart(chartTwo, {\n",
    "type: 'line',\n",
    "data: {\n",
    "labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],\n",
    "datasets: [{\n",
    "label: '# of Votes',\n",
    "data: [12, 19, 3, 5, 2, 3],\n",
    "backgroundColor: [\n",
    "'rgba(255, 99, 132, 0.2)',\n",
    "'rgba(54, 162, 235, 0.2)',\n",
    "'rgba(255, 206, 86, 0.2)',\n",
    "'rgba(75, 192, 192, 0.2)',\n",
    "'rgba(153, 102, 255, 0.2)',\n",
    "'rgba(255, 159, 64, 0.2)'\n",
    "],\n",
    "borderColor: [\n",
    "'rgba(255, 99, 132, 1)',\n",
    "'rgba(54, 162, 235, 1)',\n",
    "'rgba(255, 206, 86, 1)',\n",
    "'rgba(75, 192, 192, 1)',\n",
    "'rgba(153, 102, 255, 1)',\n",
    "'rgba(255, 159, 64, 1)'\n",
    "],\n",
    "borderWidth: 1\n",
    "}]\n",
    "},\n",
    "options: {\n",
    "scales: {"
    "yAxes: [{\n",
    "ticks: {\n",
    "beginAtZero: true\n",
    "}\n",
    "}]\n",
    "}\n",
    "}\n",
    "});\n",
    "</script>"]
    grafico = "".join(grafico)
    context = {
        'composition': instance_composition,
        'prices': instance_prices,
        'formset': formset,
        'grafico': grafico,
        'places_choices': PLACES_CHOICES,
        #'formset2': formset2, 
        }
    return render(request, 'compositions/prices_composition.html', context)
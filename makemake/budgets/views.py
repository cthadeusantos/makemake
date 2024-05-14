import re
from itertools import groupby
from operator import itemgetter

from django.db import IntegrityError
from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.utils.text import slugify
from django.db.models import Q
#from django.contrib.auth import get_user

from django.contrib.auth.models import User

from makemake.budgets.forms import *
from makemake.budgets.models import *
from makemake.agreements.models import *
from makemake.projects.models import *
from makemake.categories.models import *

from collections import defaultdict

from makemake.core.choices import BUDGETS_DATABASES_CHOICES

# Função para obter o nome correspondente ao número
def get_dbtype_name(dbtype_number):
    for number, name in BUDGETS_DATABASES_CHOICES:
        if number == dbtype_number:
            return name
    return None  # Caso o número não seja encontrado

# Create your views here

def void(request):
    return HttpResponseRedirect('')


def home(request, pk=None):
    instance = Project.objects.get(pk=pk)
    items = Agreement.objects.filter(project=instance).order_by('start')
    return render(request, 'budgets/home.html', {'items': items, 'instance': instance})




def add_or_edit(request, pk=None):
    instance_agreement = Agreement.objects.get(pk=pk)
    forms = Budget.objects.filter(agreement=instance_agreement).order_by('category__name', 'composition__description')

    if request.method == 'POST':
        chaves = request.POST.keys()
        instance_user = User.objects.get(pk=request.user.id)

        # Logica para gravar
        try:
            # Usar expressão regular para selecionar as chaves desejadas
            selected_keys = [chave for chave in chaves if re.match(r'(code|component|quantity|select-category)-\d+', chave)]
            selected_keys2 = [chave for chave in chaves if re.match(r'\d{4,}-(id|quantity)', chave)]
            values_list = []

            # Select excluded
            maintained_list_ID = []
            for item in range(0, len(selected_keys2), 2):
                value = selected_keys2[item]
                componentID = int(request.POST.get(value, ''))  # Get the component ID
                maintained_list_ID.append(componentID)
            excluded = Budget.objects.filter(agreement=instance_agreement).exclude(id__in=maintained_list_ID)

            # Select updated quantity
            maintained_list_ID = []
            for item in range(0, len(selected_keys2), 2):
                value = selected_keys2[item]
                componentID = int(request.POST.get(value, ''))  # Get the component ID
                value = selected_keys2[item + 1]
                quantity = float(request.POST.get(value, ''))
                maintained_list_ID.append((componentID, quantity))

            # Excluded list            
            auxiliary_list = [item[0] for item in maintained_list_ID]
            excluded_list = Budget.objects.filter(agreement=instance_agreement).exclude(id__in=auxiliary_list)

            # Updated list
            auxiliary_dict = {item[0]:item[1] for item in maintained_list_ID}
            updated_dict = {}
            for key, value in auxiliary_dict.items():
                quantity = Budget.objects.get(id=key).quantity
                if quantity != value:
                    updated_dict[key] = value
            del auxiliary_dict


            # Read values from HTML template
            for item in range(0, len(selected_keys), 4):
                value = selected_keys[item]
                componentID = int(request.POST.get(value, ''))  # Get the component ID
                value = selected_keys[item + 1]
                componentName = request.POST.get(value, '')  # Get the component ID
                value = selected_keys[item + 2]
                categoryID = int(request.POST.get(value, ''))   # Get the % 
                value = selected_keys[item + 3]
                quantity = float(request.POST.get(value, ''))
                #print(componentID)
                instance_composition = Composition.objects.get(code=componentID)    # The slave compositions (component from composition)
                instance_category = Category.objects.get(id=categoryID)
                values_list.append((instance_agreement, instance_composition, instance_user, instance_category, quantity))
            
            # Updated items
            user_instance = User.objects.get(id=request.user.id)
            for key, value in updated_dict.items():
                Budget.objects.filter(pk=key).update(quantity=value, user=user_instance)
            
            # Delete items
            Budget.objects.filter(id__in=excluded_list).delete()
            
            # Save items    
            for item in values_list:
                b3 = Budget(agreement=item[0], composition=item[1], user=item[2], category=item[3], quantity=item[4])
                b3.save()
        except IntegrityError as e:
            pass
   #else:
    #instance = Agreement.objects.get(pk=pk)

    # Get the related CompositionHasComponents instances
    #components = Budget.objects.filter(agreement=instance).order_by('category')
    components = forms

    # Adiciona os valores iniciais aos fields
    forms = [ComponentForm(initial={
        'id': component.id,
        'category': component.category,
        'dbtype': get_dbtype_name(component.composition.dbtype) + '/' + component.composition.code,
        'composition': component.composition.description,
        'quantity': component.quantity,
        'unit': component.composition.unit.symbol,
        'user': component.user.username,
        'userid': component.user.id,
    }, prefix=str(i+100000)) for i, component in enumerate(components)]

    # Adiciona o atributo id aos fields
    for index, form in enumerate(forms, start=100000):
        for field_name, field in form.fields.items():
            field_slug = slugify(f"{field_name}-{index}")  # Generate unique slug based on field name and index
            field_slug = field_slug.upper()
            #field_slug = field_slug.upper() if 'id-' in field_slug else field_slug
            form.fields[field_name].widget.attrs['id'] = field_slug
            if request.user.id != form.initial['userid'] and field_name == 'quantity':
                form.fields[field_name].widget.attrs['class'] += ' cursor-not-allowed'
                form.fields[field_name].widget.attrs['readonly'] = 'readonly'
            #form.fields[field_name].widget.attrs['name'] = field_slug
        
    # Build and organize fields group by category
    grouped_forms = defaultdict(list)
    for form in forms:
        grouped_forms[form['category'].initial.description].append(form)
    grouped_forms = [(category, forms) for category, forms in grouped_forms.items()] 

    context = {
            'instance': instance_agreement,
            #'forms': forms,
            'grouped_forms': grouped_forms,
        }
    return render(request, 'budgets/new_or_edit.html', context)

# class BudgetCreate(CreateView):
#     model = Budget
#     template_name = 'budgets/add.html'
#     form_class = BudgetForm
    #fields = ['quantity', 'date']

#BudgetFormSet = formset_factory(BudgetForm)

def budget_view(request):
    parent = Budget.objects.filter(id=1).first()

    if request.method == 'POST':
        formBudget = BudgetFormset(request.POST, instance=parent)
        #formset = BudgetFormSet(request.POST)
        if formBudget.is_valid():
            # Process the forms
            pass
    else:
        #formset = BudgetFormSet()
        formBudget = BudgetFormset()
    context = {
        'formset': formBudget
    }
    return render(request, 'budgets/add.html', context)


def search_categories(request):
    final_string = "Q(id__isnull=False)"
    query = "Q(id__isnull=False)"
    if query:
        results = Category.objects.filter(eval(final_string)).values('id', 'code', 'name')
        results = [{'id': result['id'], 'code': result['code'], 'name': result['name'], } for result in results]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)
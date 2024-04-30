from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from makemake.categories.models import Category
from makemake.categories.forms import CategoryForm

from django.db import IntegrityError
from django.contrib import messages

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
    items = Category.objects.all()
    return render(request, 'categories/home.html', {'items': items})

def new(request):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)

    if request.method == 'POST':    # Newly filled form
        form = CategoryForm(request.POST or None)

        if form.is_valid():
            a = form.cleaned_data['code'].upper()
            b = form.cleaned_data['name']
            c = form.cleaned_data['description']
            d = form.cleaned_data['category']

            # Logica para gravar instância principal
            b2 = Category(code=a, name=b, description=c, category=d, )
            try:
                b2.save()
            except IntegrityError as e:
                #messages.add_message(request, messages.ERROR, 'There has been an error...')
                form.add_error('code', 'Code category must be unique!')
                #context = {'form': form}
                #return render(request, 'categories/new.html', context)

    else: # Empty new form
        form = CategoryForm()

    context = {'form': form}
    return render(request, 'categories/new_or_edit.html', context)

def edit(request, pk=None):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)

    if request.method == 'POST':    # Newly filled form
        form = CategoryForm(request.POST or None)

        if form.is_valid():
            a = form.cleaned_data['code'].upper()
            b = form.cleaned_data['name']
            c = form.cleaned_data['description']
            d = form.cleaned_data['category']

            # Logica para gravar instância principal
            b2 = Category.objects.filter(pk=pk)
            b2.update(name=b, description=c, category=d)
            # # Logica para gravar instância principal
            # try:
            #     b2.save()
            # except IntegrityError as e:
            #     #messages.add_message(request, messages.ERROR, 'There has been an error...')
            #     form.add_error('code', 'Code category must be unique!')
            #     #context = {'form': form}
            #     #return render(request, 'categories/new.html', context)

    else: # Read data from 
        instance = Category.objects.get(pk=pk)
        form = CategoryForm(instance=instance, prefix='edit')

    context = {'form': form}
    return render(request, 'categories/new_or_edit.html', context)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from makemake.sites.models import Site
from makemake.sites.forms import SiteForm

from django.db import IntegrityError
from django.contrib import messages

def delete(request, pk):
    project = Site.objects.get(pk=pk)
    try:
        register_to_delete = get_object_or_404(Site, pk=pk)
        register_to_delete.delete()
    except IntegrityError:
        message = "The register couldn't be deleted!"
        messages.info(request, message)
    return home(request)
    

def home(request):
    items = Site.objects.all()
    return render(request, 'sites/home.html', {'items': items})

def new(request):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)

    if request.method == 'POST':    # Newly filled form
        form = SiteForm(request.POST or None)

        if form.is_valid():
            a = form.cleaned_data['name']
            b = form.cleaned_data['place']

            # Logica para gravar instância principal
            b2 = Site(name=a, place=b, )
            try:
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

    if request.method == 'POST':    # Newly filled form
        form = SiteForm(request.POST or None)

        if form.is_valid():
            a = form.cleaned_data['name']
            b = form.cleaned_data['place']

            # Logica para gravar instância principal
            b2 = Site.objects.filter(pk=pk)
            b2.update(name=a, place=b, )

    else: # Read data from 
        instance = Site.objects.get(pk=pk)
        form = SiteForm(instance=instance, prefix='edit')

    context = {'form': form}
    return render(request, 'sites/new_or_edit.html', context)


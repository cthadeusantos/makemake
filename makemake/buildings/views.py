from django.shortcuts import get_object_or_404, render

from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from makemake.buildings.models import Building
from makemake.buildings.forms import BuildingForm

@login_required
def home(request):
    items = Building.objects.all().order_by('number')
    return render(request, 'buildings/home.html', {'items': items})

@login_required
def delete(request, pk):
    project = Building.objects.get(pk=pk)
    try:
        register_to_delete = get_object_or_404(Building, pk=pk)
        register_to_delete.delete()
    except IntegrityError:
        message = "The register couldn't be deleted!"
        messages.info(request, message)
    return home(request)

@login_required
def new(request):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)

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
                #messages.add_message(request, messages.ERROR, 'There has been an error...')
                form.add_error('number', 'Building number must be unique!')
                #context = {'form': form}
                #return render(request, 'categories/new.html', context)

    else: # Empty new form
        form = BuildingForm(prefix='new')

    context = {'form': form}
    return render(request, 'buildings/new_or_edit.html', context)

@login_required
def edit(request, pk=None):
    #extra_forms = 1  # You can set the initial number of forms here
    #ProjectBuildingFormSet = formset_factory(ProjectBuildingForm, extra=extra_forms)

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

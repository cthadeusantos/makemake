from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.db import IntegrityError
from django.contrib import messages

from makemake.prices.models import Price, PriceLabel
from makemake.prices.forms import PriceLabelForm

def home(request):
    return render(request, 'prices/home.html', None)

def new_prices(request):
    items = Price.objects.all()
    return render(request, 'prices/new_prices.html', {'items': items})

def search_prices_labels(request):
    final_string = "Q(id__isnull=False) & Q(discontinued=False)"
    query = "Q(id__isnull=False)"
    if query:
        results = PriceLabel.objects.filter(eval(final_string)).values('id', 'reference', 'name')
        results = [{'id': result['id'], 'code': result['reference'], 'name': result['name'], } for result in results]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

def home_references(request):
    instance = PriceLabel.objects.all()
    context = {'items': instance, }
    return render(request, 'prices/home-references.html', context)

def new_reference(request):
    if request.method == 'POST':    # Newly filled form
        form = PriceLabelForm(request.POST or None)

        if form.is_valid():
            a = form.cleaned_data['name']
            b = form.cleaned_data['reference']
            c = form.cleaned_data['discontinued']
            
            a = a.lower().capitalize()

            # Logica para gravar instância principal
            b2 = PriceLabel(name=a, reference=b, discontinued=c, )
            try:
                b2.save()
                form = PriceLabelForm()
            except IntegrityError as e:
                #messages.add_message(request, messages.ERROR, 'There has been an error...')
                form.add_error('name', 'PriceLabel name must be unique!')
                #context = {'form': form}
                #return render(request, 'categories/new.html', context)

    else: # Empty new form
        form = PriceLabelForm()

    context = {'form': form}
    return render(request, 'prices/new_or_edit_reference.html', context)

def add_or_edit_reference(request, pk=None):
    if request.method == 'POST':    # Newly filled form
        #instance = PriceLabel.objects.get(pk=pk)
        #form = PriceLabelForm(request.POST or None, instance=instance)
        form = PriceLabelForm(request.POST or None)
        #form.fields['name'].widget.attrs['readonly'] = True
        if form.is_valid():
            a = form.cleaned_data['name']
            b = form.cleaned_data['reference']
            c = form.cleaned_data['discontinued']
            
            a = a.upper()

            # Logica para gravar instância principal
            if pk is None:
                b2 = PriceLabel(name=a, reference=b, discontinued=c, )
                try:
                    b2.save()
                    form = PriceLabelForm()
                except IntegrityError as e:
                    #messages.add_message(request, messages.ERROR, 'There has been an error...')
                    form.add_error('name', 'PriceLabel name must be unique!')
                    #context = {'form': form}
                    #return render(request, 'categories/new.html', context)
            else:
                # Logica para gravar instância principal editada
                try:
                    b2 = PriceLabel.objects.filter(pk=pk)
                    b2.update(name=a, reference=b, discontinued=c,)
                    form = PriceLabelForm()
                except IntegrityError:
                    pass
        # else:
        #     #a = form.cleaned_data['name']
        #     #b = form.cleaned_data['reference']
        #     c = form.cleaned_data['discontinued']
            
        #     #a = a.lower().capitalize()

        #     # Logica para gravar instância principal
        #     b2 = PriceLabel(discontinued=c, )
        #     #try:
        #     b2.save()
        #     form = PriceLabelForm()
        #     #except IntegrityError as e:
        #         #messages.add_message(request, messages.ERROR, 'There has been an error...')
        #         #form.add_error('name', 'PriceLabel name must be unique!')
        #         #context = {'form': form}
        #         #return render(request, 'categories/new.html', context)


    else: # Empty new form
        if pk is not None:
            instance = PriceLabel.objects.get(pk=pk)
            form = PriceLabelForm(instance=instance)
        else:
            form = PriceLabelForm()

    context = {'form': form}
    return render(request, 'prices/new_or_edit_reference.html', context)

def delete_reference(request, pk):
    register_to_delete = PriceLabel.objects.get(pk=pk)
    try:
        register_to_delete.delete()
    except IntegrityError:
        message = "The register couldn't be deleted!"
        messages.info(request, message)
    return home_references(request)

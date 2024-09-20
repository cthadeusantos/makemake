from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q

from makemake.prices.models import Price, PriceLabel

def home(request):
    items = Price.objects.all()
    return render(request, 'prices/home.html', {'items': items})

def search_prices_labels(request):
    final_string = "Q(id__isnull=False) & Q(discontinued=False)"
    query = "Q(id__isnull=False)"
    if query:
        results = PriceLabel.objects.filter(eval(final_string)).values('id', 'reference', 'name')
        results = [{'id': result['id'], 'code': result['reference'], 'name': result['name'], } for result in results]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

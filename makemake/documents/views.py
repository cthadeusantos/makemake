from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelChoiceField
from django.utils import formats
from django.db.models import Q, F, Window, Subquery
from django.db.models.functions import RowNumber
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required

import os
import tempfile
import zipfile
import re

from makemake.buildings.models import Building
from makemake.categories.models import Category
from makemake.documents.forms import DocumentForm2, VersionForm
from makemake.documents.models import Document, Version
from makemake.projects.models import Project

from makemake.core.custom_functions import extract_filename, is_list_empty, separar_valores_sem_espaco, get_status_label, replace_string
from makemake.core.choices import DOCUMENT_STATUS_CHOICES_CODE_FOR_FILES, FILE_EXTENSION

from django.db.models import Max, Count

def search(request, pk):
    # Expressão regular
    # String de exemplo
    # string = "   123   /   456  "

    regex = r"^\s*(\d+)\s*\/\s*(\d+)\s*$"

    # Texto de consulta enviado através do formulário
    input_text = request.GET.get('search', None)

    if input_text == '' or input_text is None:
        items = Document.objects.all().order_by('-docstatus', 'building', 'doctype', 'categories', 'summary')
        return render(request, 'documents/home.html', {'items': items})

    # Verifica se a string corresponde ao padrão
    match = re.match(regex, input_text)

    if match: # Check if pattern is code / year
        x = int(match.group(1))  # Captura o valor de X
        y = int(match.group(2))  # Captura o valor de Y

        # Usa Q objects para filtrar o modelo
        items = Document.objects.filter(Q(code=x) & Q(year=y))
    else:   # Pattern is a free string
        and_list, or_list = separar_valores_sem_espaco(input_text)
        if is_list_empty(and_list) and is_list_empty(or_list):
            items = Document.objects.filter(Q(summary__icontains=input_text)).order_by('-docstatus', 'building', 'doctype', 'categories', 'summary')
        else:
            ### FUNCAO ABAIXO NÃO ESTA FUNCIONANDO
            ### PRECISA REFATORAR PARA FICAR MUITO MELHOR
            string_and = ''
            string_or = ''
            pattern = 'Q(summary__icontains='
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
            items = Document.objects.filter(eval(final_string)).order_by('-docstatus', 'building', 'doctype', 'categories', 'summary')
    instance = Project.objects.get(pk=pk)
    return render(request, 'documents/home.html', {'items': items, 'instance': instance})

def void(request):
    return HttpResponseRedirect('')

def home(request, pk=None):
    instance = Project.objects.get(pk=pk)
    items = Document.objects.filter(project=instance).order_by( '-docstatus', '-created_at', 'building', 'doctype', 'categories', '-sequential', 'summary')
    return render(request, 'documents/home.html', {'items': items, 'instance': instance})

def new(request, numproject=None):
    if request.method == 'POST':
        form = DocumentForm2(request.POST, numproject=numproject, prefix='repost')

        if form.is_valid():
            a = form.cleaned_data['building'].id
            b = form.cleaned_data['categories'].id
            c = form.cleaned_data['summary']
            d = form.cleaned_data['description']
            e = form.cleaned_data['created_at']
            f = form.cleaned_data['updated_at']
            g = form.cleaned_data['doctype']
            h = form.cleaned_data['docstatus']
            data = {
                'a': a,
                'b': b,
                'c': c,
                'd': d,
                'e': e,
                'f': f,
                'g': g,
                'h': h,
                'instance_project': Project.objects.get(id=numproject),
                'instance_building': Building.objects.get(id=a),
                'instance_category': Category.objects.get(id=b),
            }

            try:
                query = Document.objects.filter(
                    Q(doctype=data.g) &
                    Q(docstatus=data.h) &
                    Q(project=data.instance_temp) &
                    Q(building=data.instance_building) &
                    Q(categories=data.instance_category)
                    )
                # Recuperar o maior valor de released para o conjunto filtrado
                last = query.aggregate(last_sequential=Max('last_sequential'))['last_sequential'] + 1
 
                instance = Document(summary=c,
                                    description=d,
                                    created_at=e,
                                    updated_at=f,
                                    doctype=g,
                                    docstatus=h,
                                    project=data.instance_project,
                                    building=data.instance_building,
                                    categories=data.instance_category,
                                    )
                instance.save()
                print("LAST!", last)
            except:
                last = 0
            #reserve_doc_number(data)
            return HttpResponseRedirect('/documents/new/' + str(numproject))
    context = {'form': DocumentForm2(numproject=numproject, prefix='new'),
                'numproject': numproject}
    return render(request, 'documents/new_or_edit.html', context)

def edit(request, pk=None, numproject=None):
    if pk:
        document = Document.objects.get(pk=pk)
        if request.method == "POST":
            form = DocumentForm2(request.POST, instance=document)
            #category_formset = DocCategoryFormSet(request.POST, prefix='categories')
            if form.is_valid():
                a = form.cleaned_data['summary']
                b = form.cleaned_data['description']
                c = form.cleaned_data['updated_at']
                d = form.cleaned_data['doctype']
                
                # Logica para gravar instância principal
                b2 = Document.objects.filter(pk=pk)
                b2.update(summary=a, description=b, updated_at=c, doctype=d, )
                items = Building.objects.all().order_by('number')
                
                instance = Project.objects.get(pk=numproject)
                items = Document.objects.filter(project=instance)
                context = {
                    'items': items,
                    'numproject': pk,
                    'instance': instance,
                    }
                return render(request, 'documents/home.html', context)
                # return render(request, 'buildings/home.html', {'items': items})
                # return HttpResponseRedirect('/documents/edit/' + str(pk))
            else:
                #return render(request, 'documents/edit.html')
                form.add_error('summary', 'form submission error!')

        queryset = Building.objects.prefetch_related('buildings').filter(buildings__id=numproject)
        building = ModelChoiceField(queryset)

        context = {'form': DocumentForm2(instance=document, building=building, prefix='edit'),
                    'pk': pk,
                    'numproject': numproject}
        
        return render(request, 'documents/new_or_edit.html', context)



def details(request, pk):
    context = prepare_details_context(pk)
    return render(request, 'documents/details.html', context)

@staticmethod
def prepare_details_context(pk):
    document = get_object_or_404(Document, pk=pk)
    versions = Version.objects.filter(document=document).order_by('-upload_at', '-released')
    for version in versions:
        version.upload_url.name = extract_filename(version.upload_url.name)
        version.upload_at = formats.date_format(version.upload_at, format='SHORT_DATE_FORMAT')
    numproject = document.project.id
    filename = set_filename(document)
    return {'document': document, 'versions': versions, 'numproject': numproject, 'filename': filename}

def delete(request, pk):
    instance = get_object_or_404(Document, id=pk)
    numproject = instance.project.pk
    instance.delete()
    return redirect('home-documents', numproject)

def version(request, pk=None):
    document_instance = Document.objects.get(pk=pk)
    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES, pk=pk)
        if form.is_valid():
            a = form.cleaned_data['released']
            b = form.cleaned_data['changelog']
            c = form.cleaned_data['upload_at']
            d = form.cleaned_data['upload_url'].upper()
            version = Version(released=a,
                              changelog=b,
                              upload_at=c,
                              upload_url=d,
                              document=document_instance)
            filename = get_filename(document_instance, a)
            if filename == d.name:
                version = Version.objects.filter(pk=pk).update(
                    changelog=b,
                    upload_at=c,
                    upload_url=d,
                    )
                context = prepare_details_context(document_instance.pk)
                return render(request, 'documents/details.html', context)
            else:
                form.add_error('upload_url', 'form submission error - invalid filename!')
                context = {'form': form, 'pk': document_instance, 'filename': filename, 'url': version.upload_url}
                return render(request, 'documents/version.html', context)
        else:
            a = form.cleaned_data['released']
            b = form.cleaned_data['changelog']
            c = form.cleaned_data['upload_at']
            filename = get_filename(document_instance, a)

            try:
                d = form.cleaned_data['upload_url'].upper().name
                if filename == d:
                    version = Version.objects.filter(
                        Q(document_pk=pk) & 
                        Q(released=a)).update(
                            changelog=b,
                            upload_at=c,
                            upload_url=d,
                            document=document_instance,
                            )
                    context = prepare_details_context(document_instance.pk)
                    return render(request, 'documents/details.html', context)
                else:
                    form.add_error('upload_url', 'form submission error - invalid filename!')
                    context = {
                        'form': form,
                        'pk': version.document.pk,
                        'filename': filename,
                        'url': version.upload_url
                        }
                    return render(request, 'documents/version.html', context)
            except KeyError:
                version = Version.objects.filter(Q(document_id=pk) & Q(released=a)).update(
                    changelog=b,
                    upload_at=c,
                    document=document_instance,
                    )
                context = prepare_details_context(document_instance.pk)
                return render(request, 'documents/details.html', context)

    query = Version.objects.select_related('document')
    
    # Recuperar o maior valor de released para o conjunto filtrado
    max_sequential = query.filter(document__pk=pk).aggregate(max_version=Count('released'))['max_version']
    query3 = query.filter(Q(document__pk=pk) & 
                          Q(released=max_sequential) & 
                          Q(upload_url__isnull=True)
                          ).exists()

    if query3 or (not query3 and not max_sequential):
        filename, sequential = adjust_filename3(document_instance, max_sequential, pattern=r'-\w{2}(?=\.\w+$)', nmask='00')
        Version.objects.create(
            released=sequential,
            document=document_instance,
        )
    else:
        context = prepare_details_context(pk)
        context['error'] = 1 # Adiciona Lógica específica para esta view abrir janela JS no template
        return render(request, 'documents/details.html', context)

    form = VersionForm(pk=pk, sequential=sequential)
    context = {'form': form, 'pk': pk, 'filename': filename}
    return render(request, 'documents/version.html', context)

def edit_version(request, pk=None):
    version_instance = Version.objects.get(pk=pk)
    document_instance = version_instance.document
    document_pk = version_instance.document.pk
    # Recuperar o maior valor de released para o conjunto filtrado
    #max_released = query.aggregate(max_version=Max('released'))['max_version']
    version = version_instance.released
    #filename, sequential = adjust_filename2(document_instance, version, pattern=r'-\w{2}(?=\.\w+$)', nmask='00')
    filename = get_filename(document_instance, version, pattern=r'-\w{2}(?=\.\w+$)', nmask='00')
    
    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES, pk=document_pk)
        if form.is_valid():
            a = form.cleaned_data['released']
            b = form.cleaned_data['changelog']
            c = form.cleaned_data['upload_at']
            d = form.cleaned_data['upload_url'].upper()
            if filename == d.name:
                version = Version.objects.filter(pk=pk).update(
                    changelog=b,
                    upload_at=c,
                    upload_url=d,
                    )
                context = prepare_details_context(version_instance.document.pk)
                return render(request, 'documents/details.html', context)
                #return HttpResponseRedirect('/documents/details/' + str(version_instance.document.pk))
            else:
                form.add_error('upload_url', 'form submission error - invalid filename!')
                context = {'form': form, 'pk': document_pk, 'filename': filename, 'url': version_instance.upload_url}
                return render(request, 'documents/version.html', context)
        else:
            if filename == d.name:
                a = form.cleaned_data['released']
                b = form.cleaned_data['changelog']
                c = form.cleaned_data['upload_at']
                version = Version.objects.filter(pk=pk).update(
                    changelog=b,
                    upload_at=c,
                    )
                context = prepare_details_context(version_instance.document.pk)
                return render(request, 'documents/details.html', context)
                #return HttpResponseRedirect('/documents/details/' + str(version_instance.document.pk))
            else:
                form.add_error('upload_url', 'form submission error - invalid filename!')
                context = {'form': form, 'pk': document_pk, 'filename': filename, 'url': version_instance.upload_url}
                return render(request, 'documents/version.html', context)

    form = VersionForm(pk=document_pk, sequential=version, instance=version_instance)
    context = {'form': form, 'pk': document_pk, 'filename': filename, 'url': version_instance.upload_url}
    return render(request, 'documents/version.html', context)

@staticmethod
def download_file(request, file_id):
    uploaded_file = Version.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.upload_url, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.upload_url.name}"'
    return response

@staticmethod
def download_files(request, numproject=None):
    # Com o ID do projeto em 'numproject'
    # Subconsulta para obter as últimas versões dos documentos para o projeto específico
    latest_versions_subquery = Version.objects.filter(document__project_id=numproject) \
        .annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=[F('document_id')],
                order_by=F('released').desc()
            )
        ) \
        .filter(row_number=1) \
        .values('id')

    # Obter os registros correspondentes às últimas versões dos documentos para o projeto específico
    latest_records = Version.objects.filter(id__in=Subquery(latest_versions_subquery))

    # Criar arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(delete=True)
    with zipfile.ZipFile(temp_file, 'w') as zipf:
        # Adicione cada arquivo ao arquivo ZIP
        for uploaded_file in latest_records:
            zipf.write(uploaded_file.upload_url.path, os.path.basename(uploaded_file.upload_url.path))

    # Volte ao início do arquivo temporário antes de ler
    temp_file.seek(0)

    # Cria uma resposta HTTP com o arquivo ZIP
    response = HttpResponse(temp_file.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="files.zip"'

    # Fecha o arquivo temporário
    temp_file.close()

    return response

# @staticmethod    
# def get_next_doc_number(category,building, doctype, docstatus):
#     """
#     Calcula o próximo número sequencial para uma combinação específica.
#     """
#     # Buscar o maior número já reservado para a combinação
#     x =0 
#     last_number = (
#         Document.objects.filter(
#             categories=category,
#             building=building,
#             doctype=doctype,
#             docstatus=docstatus
#         )
#         .aggregate(max_number=Max('sequential'))['max_number']
#     )

#     # Se nenhum número existir, começar com 1; caso contrário, incrementar
#     return (last_number or 0) + 1

@staticmethod
def set_filename(document):
    building = mask(document.building.number)
    sequential = mask(document.sequential)
    status = get_status_label(document.docstatus, DOCUMENT_STATUS_CHOICES_CODE_FOR_FILES)
    extension = get_status_label(document.doctype, FILE_EXTENSION)
    return f'{document.categories.code}{building}{status}{sequential}-XX.{extension}'

@staticmethod
def mask(value, mask='0000'):
    # Constroi string a partir do número do prédio
    #string = f"{building:0{len(mask)}}" # For python 3.6+
    return str(value).zfill(len(mask)) # For all Python versions

@staticmethod
def adjust_filename2(instance, sequential, pattern=r'-\w{2}(?=\.\w+$)', nmask='00'):
    str_sequential = mask(sequential, nmask)
    filename = set_filename(instance)
    pattern = re.compile(pattern)
    return replace_string(filename, str_sequential, pattern), sequential

@staticmethod
def adjust_filename3(document_instance, sequential, pattern=r'-\w{2}(?=\.\w+$)', nmask='00'):
    sequential = next_sequential(sequential)
    str_sequential = mask(sequential, nmask)
    filename = set_filename(document_instance)
    pattern = re.compile(pattern)
    return replace_string(filename, str_sequential, pattern), sequential

@staticmethod
def get_filename(document_instance, sequential=0, pattern=r'-\w{2}(?=\.\w+$)', nmask='00'):
    if type(sequential) == str:
        sequential = int(sequential)
    sequential = mask(sequential, nmask)
    filename = set_filename(document_instance)
    pattern = re.compile(pattern)
    return replace_string(filename, sequential, pattern)

@staticmethod
def next_sequential(sequential):
    # Se nenhum número existir, começar com 1; caso contrário, incrementar
    return (sequential or 0) + 1
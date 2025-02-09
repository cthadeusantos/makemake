from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelChoiceField
from django.utils import formats
from django.db.models import Q, F, Window, Subquery
from django.db.models.functions import RowNumber
from django.db import IntegrityError
from django.core.exceptions import FieldError    

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

from makemake.core.custom_functions import extract_filename, is_list_empty, separar_valores_sem_espaco, get_status_label, replace_string, is_queryset_empty, create_or_update_object
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
    items = Document.objects.filter(project=instance).order_by( '-docstatus', 'building', 'doctype', 'categories', '-created_at', '-sequential', 'summary')
    return render(request, 'documents/home.html', {'items': items, 'instance': instance})

def new(request, numproject=None):
    if request.method == 'POST':
        form = DocumentForm2(request.POST, numproject=numproject, prefix='repost')

        if form.is_valid():
            a = form.cleaned_data['building'].id
            b = form.cleaned_data['categories'].id
            data = {
                'summary': form.cleaned_data['summary'],
                'description': form.cleaned_data['description'],
                'created_at': form.cleaned_data['created_at'],
                'updated_at': form.cleaned_data['updated_at'],
                'doctype': form.cleaned_data['doctype'],
                'docstatus': form.cleaned_data['docstatus'],
                'project': Project.objects.get(id=numproject),
                'building': Building.objects.get(id=a),
                'categories': Category.objects.get(id=b),
            }

            try:
                query = Document.objects.filter(
                    Q(doctype=data['doctype']) &
                    Q(docstatus=data['docstatus']) &
                    Q(project=data['project']) &
                    Q(building=data['building']) &
                    Q(categories=data['categories'])
                    )
                
                # Recuperar o maior valor de released para o conjunto filtrado
                if is_queryset_empty(query):
                    last = 1
                else:
                    last = query.aggregate(sequential=Max('sequential'))['sequential'] + 1
                data['sequential'] = last

                b2 = create_or_update_object(request, Document, data)
            except:
                
                # OOPS! Some error ocurred 
                document = Document()
                context = {'document': document, }
                return render(request, 'page_error.html', context)
            
            return HttpResponseRedirect('/documents/new/' + str(numproject))
    context = {'form': DocumentForm2(numproject=numproject, prefix='new'),
                'numproject': numproject}
    return render(request, 'documents/new_or_edit.html', context)

"""
Document Edit
"""
def edit(request, pk=None, numproject=None):
    if pk:
        document = Document.objects.get(pk=pk)
        if request.method == "POST":
            form = DocumentForm2(request.POST, instance=document)
            if form.is_valid():
                data = {
                    'summary': form.cleaned_data['summary'],
                    'description': form.cleaned_data['description'],
                    'updated_at': form.cleaned_data['updated_at'],
                    'doctype': form.cleaned_data['doctype'],
                }
                
                # Logica para gravar instância principal
                b2 = create_or_update_object(request, Document, data, pk)
                
                items = Building.objects.all().order_by('number')
                
                instance = Project.objects.get(pk=numproject)
                items = Document.objects.filter(project=instance)
                context = {
                    'items': items,
                    'numproject': pk,
                    'instance': instance,
                    }
                return render(request, 'documents/home.html', context)
            else:
                form.add_error('summary', 'form submission error!')

        context = {'form': DocumentForm2(instance=document, pk=pk, prefix='edit'),
                   'numproject': document.project.pk}
        
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
            data = {
                'released': form.cleaned_data['released'],
                'changelog': form.cleaned_data['changelog'],
                'upload_at': form.cleaned_data['upload_at'],
                'upload_url': form.cleaned_data['upload_url'],
            }

            filename = get_filename(document_instance, data['released'])

            if filename.upper() == data['upload_url'].name.upper():
                version_pk = Version.objects.get(Q(document=document_instance) & Q(released=data['released'])).pk
                b2 = create_or_update_object(request, Version, data, version_pk)

                context = prepare_details_context(document_instance.pk)
                return render(request, 'documents/details.html', context)
            else:
                form.add_error('upload_url', 'form submission error - invalid filename!')
                context = {'form': form, 'pk': document_instance, 'filename': filename, 'url': version.upload_url}
                return render(request, 'documents/version.html', context)
        else:

            data = {
                'released': form.cleaned_data['released'],
                'changelog': form.cleaned_data['changelog'],
                'upload_at': form.cleaned_data['upload_at'],
            }
            filename = get_filename(document_instance, data['released'])


            try:
                data['upload_url'] = form.cleaned_data['upload_url']

                if filename.upper() == data['upload_url'].name.upper():
                    version_pk = Version.objects.get(Q(document__pk=pk) & Q(released=data['released'])).pk
                    b2 = create_or_update_object(request, Version, data, version_pk)
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
                
            except (KeyError, FieldError):
                version_pk = Version.objects.get(Q(document__pk=pk) & Q(released=data['released'])).pk
                b2 = create_or_update_object(request, Version, data, version_pk)
                context = prepare_details_context(document_instance.pk)
                return render(request, 'documents/details.html', context)
    
    # Recuperar o maior valor de released para o conjunto filtrado
    max_sequential = Version.objects.filter(document__pk=pk).values_list('released', flat=True).order_by('-released').first()
    query3 = Version.objects.filter(document=document_instance, released=max_sequential, upload_url__isnull=False).exists()

    if not query3 or (not query3 and not max_sequential):
        filename, sequential = adjust_filename3(document_instance, max_sequential, pattern=r'-\w{2}(?=\.\w+$)', nmask='00')
        data = {
            'released': sequential,
            'document': document_instance,
        }
        b2 = create_or_update_object(request, Version, data)
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
    version = version_instance.released
    filename = get_filename(document_instance, version, pattern=r'-\w{2}(?=\.\w+$)', nmask='00')
    
    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES, pk=document_pk)

        if form.is_valid():
            data = {
                'released': form.cleaned_data['released'],
                'changelog': form.cleaned_data['changelog'],
                'upload_at': form.cleaned_data['upload_at'],
                'upload_url': form.cleaned_data['upload_url'],
            }

            if filename.upper() == data['upload_url'].name.upper():
                version_pk = Version.objects.get(Q(document_pk=pk) & Q(released=data['released'])).pk
                b2 = create_or_update_object(request, Version, data, version_pk)
                context = prepare_details_context(version_instance.document.pk)
                return render(request, 'documents/details.html', context)
            else:
                form.add_error('upload_url', 'form submission error - invalid filename!')
                context = {'form': form, 'pk': document_pk, 'filename': filename, 'url': version_instance.upload_url}
                return render(request, 'documents/version.html', context)            
        else:
            if filename.upper() == data['upload_url'].name.upper():
                data = {
                    'released': form.cleaned_data['released'],
                    'changelog': form.cleaned_data['changelog'],
                    'upload_at': form.cleaned_data['upload_at'],
                }
                version_pk = Version.objects.get(Q(document_pk=pk) & Q(released=data['released'])).pk
                b2 = create_or_update_object(request, Version, data, version_pk)
                context = prepare_details_context(version_instance.document.pk)
                return render(request, 'documents/details.html', context)
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
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelChoiceField
from django.utils import formats
from django.db.models import Q, F, Window, Subquery
from django.db.models.functions import RowNumber

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

from makemake.core.custom_functions import extract_filename, is_list_empty, separar_valores_sem_espaco


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
    items = Document.objects.filter(project=instance).order_by('-docstatus', 'building', 'doctype', 'categories', 'summary')
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
            instance_temp = Project.objects.get(id=numproject)
            instance_building = Building.objects.get(id=a)
            instance_category = Category.objects.get(id=b)
            instance = Document(summary=c,
                                description=d,
                                created_at=e,
                                updated_at=f,
                                doctype=g,
                                docstatus=h,
                                project=instance_temp,
                                building=instance_building,
                                categories=instance_category,
                                )
            instance.save()
            #return HttpResponseRedirect('/documents/new/' + str(numproject))
    context = {'form': DocumentForm2(numproject=numproject, prefix='new'),
                #'category_formset': DocCategoryFormSet(prefix='categories'),
                #'building_formset': DocBuildingFormSet(prefix='buildings'),
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
                return render(request, 'documents/home.html', {'items': items, 'numproject': pk})
                # return render(request, 'buildings/home.html', {'items': items})
                # return HttpResponseRedirect('/documents/edit/' + str(pk))
            else:
                #return render(request, 'documents/edit.html')
                form.add_error('summary', 'form submission error!')
        queryset = Building.objects.prefetch_related('buildings').filter(buildings__id=numproject)
        building = ModelChoiceField(queryset)
        context = {'form': DocumentForm2(instance=document, building=building, prefix='edit'),
                    #'category_formset': DocCategoryFormSet(prefix='categories'),
                    'pk': pk,
                    'numproject': numproject}
        return render(request, 'documents/new_or_edit.html', context)

#
def details(request, pk):
    document = Document.objects.get(pk=pk)
    versions = Version.objects.filter(document=document).order_by('-upload_at', '-version_number')
    for version in versions:
        version.upload_url.name = extract_filename(version.upload_url.name)
        version.upload_at = formats.date_format(version.upload_at, format='SHORT_DATE_FORMAT')
        #version.upload_at = version.upload_at.strftime('%Y-%m-%d')
    numproject = document.project.id
    context = {'document': document, 'versions': versions, 'numproject': numproject}
    return render(request, 'documents/details.html', context)


def delete(request, pk):
    instance = get_object_or_404(Document, id=pk)
    numproject = instance.project.pk
    instance.delete()
    return redirect('home-documents', numproject)


def version(request, pk=None):
    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES, pk=pk)
        if form.is_valid():
            a = form.cleaned_data['version_number']
            b = form.cleaned_data['changelog']
            c = form.cleaned_data['upload_at']
            d = form.cleaned_data['upload_url']
            document_instance = Document.objects.get(pk=pk)
            version = Version(version_number=a,
                              changelog=b,
                              upload_at=c,
                              upload_url=d,
                              document=document_instance)
            version.save()
            return HttpResponseRedirect('/documents/details/' + str(pk))
    context = {'form': VersionForm(pk=pk), 'pk': pk}
    return render(request, 'documents/version.html', context)

#
def download_file(request, file_id):
    uploaded_file = Version.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.upload_url, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.upload_url.name}"'
    return response

def download_files(request, numproject=None):
    # Com o ID do projeto em 'numproject'
    # Subconsulta para obter as últimas versões dos documentos para o projeto específico
    latest_versions_subquery = Version.objects.filter(document__project_id=numproject) \
        .annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=[F('document_id')],
                order_by=F('version_number').desc()
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

    # for fileid in latest_records:
    #     #uploaded_file = Version.objects.filter(document__project_id=numproject)
    #     idfile=fileid.id
    #     uploaded_file = Version.objects.get(id=idfile)
    #     response = HttpResponse(uploaded_file.upload_url, content_type='application/force-download')
    #     response['Content-Disposition'] = f'attachment; filename="{uploaded_file.upload_url.name}"'
    # return response
    # def upload_file(request):
    #     if request.method == 'POST':
    #         form = UploadFileForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('upload_file')
    #     else:
    #         form = UploadFileForm()
    #     files = UploadedFile.objects.all()
    #     return render(request, 'upload_file.html', {'form': form, 'files': files})


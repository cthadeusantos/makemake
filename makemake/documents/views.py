from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelChoiceField
from django.utils import formats

from django.db.models import Max
from django.contrib.auth.decorators import login_required

from makemake.buildings.models import Building
from makemake.categories.models import Category
from makemake.documents.forms import DocumentForm2, VersionForm
from makemake.documents.models import Document, Version
from makemake.projects.models import Project

def extract_filename(url):
    return url.split('/')[-1]

@login_required
def void(request):
    return HttpResponseRedirect('')

@login_required
def home(request, pk=None):
    instance = Project.objects.get(pk=pk)
    items = Document.objects.filter(project=instance)
    return render(request, 'documents/home.html', {'items': items, 'numproject': pk})


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
            instance_temp = Project.objects.get(id=numproject)
            instance_building = Building.objects.get(id=a)
            instance_category = Category.objects.get(id=b)
            instance = Document(summary=c,
                                description=d,
                                created_at=e,
                                updated_at=f,
                                doctype=g,
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
                b2.update(summary=a, description=b, updated_at=c, doctype=d)
                items = Building.objects.all().order_by('number')
                
                instance = Project.objects.get(pk=numproject)
                items = Document.objects.filter(project=instance)
                return render(request, 'documents/home.html', {'items': items, 'numproject': pk})
                return render(request, 'buildings/home.html', {'items': items})
                return HttpResponseRedirect('/documents/edit/' + str(pk))
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

#@login_required
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

@login_required
def delete(request, pk):
    instance = get_object_or_404(Document, id=pk)
    numproject = instance.project.pk
    instance.delete()
    return redirect('home-documents', numproject)

@login_required
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

#@login_required
def download_file(request, file_id):
    uploaded_file = Version.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.upload_url, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.upload_url.name}"'
    return response

def download_files(request, numproject=None):
    # Supondo que você tenha o ID do projeto em 'numproject'
    # Primeiro, obtenha a maior versão para cada categoria de documento do projeto
    latest_versions = Version.objects.filter(document__project_id=numproject)\
        .values('document__categories')\
        .annotate(max_version=Max('version_number'))

    # Em seguida, obtenha os registros correspondentes com essas maiores versões
    latest_records = Version.objects.filter(document__project_id=numproject,
                                            version_number__in=latest_versions.values('max_version'))
    for fileid in latest_records:
        #uploaded_file = Version.objects.filter(document__project_id=numproject)
        idfile=fileid.id
        uploaded_file = Version.objects.get(id=idfile)
        response = HttpResponse(uploaded_file.upload_url, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.upload_url.name}"'
    return response
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


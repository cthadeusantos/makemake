from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import ModelChoiceField

from makemake.buildings.models import Building
from makemake.documents.forms import DocumentForm, DocumentForm2, VersionForm, DocCategoryFormSet, DocBuildingFormSet
from makemake.documents.models import Document, Version
from makemake.projects.models import Project


def void(request):
    return HttpResponseRedirect('')


def home(request, pk=None):
    instance = Project.objects.get(pk=pk)
    items = Document.objects.filter(project=instance)
    return render(request, 'documents/home.html', {'items': items, 'project_number': pk})


def new(request, project_number=None):
    if request.method == 'POST':
        form = DocumentForm2(request.POST, project_number=project_number)
        category_formset = DocCategoryFormSet(request.POST)
        #form = DocumentForm(request.POST, prefix='documents')
        #category_formset = DocCategoryFormSet(request.POST, prefix='categories')
        
        # # Enabled fields
        # form.fields['created_at'].disabled = True
        # form.fields['updated_at'].disabled = True

        if category_formset.is_valid() and form.is_valid():
            instance_temp = Project.objects.get(id=project_number)
            instance_building = Building.objects.get(id=context['building'])
            instance = Document(summary=form['summary'],
                                description=form['description'],
                                created_at=form['created_at'],
                                updated_at=form['updated_at'],
                                #doctype=data['doctype'],
                                project=instance_temp,
                                building=instance_building,
                                )
            # context = {'project_number': project_number,
            #            'category_formset': category_formset,
            #            'building': form.data['documents-building']}
            form.save(instance)
            return HttpResponseRedirect('/documents/new/' + str(project_number))
        else:
            context = {'form': DocumentForm(prefix='documents'),
                       'category_formset': DocCategoryFormSet(prefix='categories'),
                       'project_number': project_number}
            return render(request, 'documents/new.html', context)
    else:
        #queryset = Building.objects.prefetch_related('buildings').filter(buildings__id=project_number)
        #building = ModelChoiceField(queryset)
        context = {'form': DocumentForm2(project_number=project_number, prefix='documents'),
                   'category_formset': DocCategoryFormSet(prefix='categories'),
                   'building_formset': DocBuildingFormSet(prefix='buildings'),
                   'project_number': project_number}
        return render(request, 'documents/new.html', context)


def edit(request, pk=None, project_number=None):
    if pk:
        document = Document.objects.get(pk=pk)
        if request.method == "POST":
            form = DocumentForm(request.POST, instance=document)
            category_formset = DocCategoryFormSet(request.POST, prefix='categories')
            if form.is_valid() and category_formset.is_valid():
                context = {'pk': pk,
                           'project_number': project_number,
                           'category_formset': category_formset}
                form.update(context)
                return HttpResponseRedirect('/documents/edit/' + str(pk))
            else:
                return render(request, 'documents/edit.html')
        else:
            queryset = Building.objects.prefetch_related('buildings').filter(buildings__id=project_number)
            building = ModelChoiceField(queryset)
            context = {'form': DocumentForm(instance=document, building=building),
                       'category_formset': DocCategoryFormSet(prefix='categories'),
                       'pk': pk,
                       'project_number': project_number}
            return render(request, 'documents/edit.html', context)


def details(request, pk):
    document = Document.objects.get(pk=pk)
    versions = Version.objects.filter(document=document)
    project_number = document.project.id
    context = {'document': document, 'versions': versions, 'project_number': project_number}
    return render(request, 'documents/details.html', context)


def delete(request, pk):
    instance = get_object_or_404(Document, id=pk)
    project_number = instance.project.pk
    instance.delete()
    return redirect('home-documents', project_number)


def version(request, pk=None):
    if request.method == 'POST':
        form = VersionForm(request.POST, request.FILES, pk=pk)
        if form.is_valid():
            form.save(pk)
            return HttpResponseRedirect('/documents/details/' + str(pk))
        else:
            context = {'form': VersionForm(pk=pk), 'pk': pk}
            return render(request, 'documents/version.html', context)
    else:
        context = {'form': VersionForm(pk=pk), 'pk': pk}
        return render(request, 'documents/version.html', context)


def download_file(request, file_id):
    uploaded_file = Version.objects.get(pk=file_id)
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


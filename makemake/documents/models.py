import os
from datetime import date

from django.db.models import Q
from django.db import models
from makemake.projects.models import Project
from makemake.categories.models import Category
from makemake.buildings.models import Building
from makemake.core.custom_functions import left_pad


class Document(models.Model):
    summary = models.TextField(default='', max_length=100)
    description = models.TextField(default='')
    created_at = models.DateField(default=date.today, editable=True)
    updated_at = models.DateField(default=date.today, editable=True)
    project = models.ForeignKey(Project,
                                related_name='project',
                                on_delete=models.PROTECT,
                                blank=True,
                                null=True,
                                )
    building = models.ForeignKey(Building,
                                 related_name='docbuilding',
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True,
                                 )
    #doctype = models.PositiveSmallIntegerField(null=False)
    #categories = models.ManyToManyField(Category, related_name='categories')
    categories = models.ForeignKey(Category,
                                   related_name='categories',
                                   on_delete=models.PROTECT,
                                   blank=True,
                                   null=True,
                                )
    objects = models.Manager()

    def __str__(self):
        return self.summary

class Version(models.Model):
    def create_path(instance, filename):
        return os.path.join(
            'upload/',
            instance.building,
            '/%Y/%m/%d/',
            filename
        )

    def directory_path(self, filename):
        project_number = self.document.project.pk
        category = self.document.categories.get(Q(categories__project=project_number) & Q(category__isnull=True))
        category_code = category.code
        building = self.document.building.pk
        project_number = left_pad(project_number)
        building_number = left_pad(building)
        #path = '{0}/{1}/{2}'.format(
        path = '{0}/{1}/{2}/{3}'.format(
            building_number,
            project_number,
            category_code,
            filename
        )
        return path

    version_number = models.IntegerField(default=1,)
    changelog = models.TextField(default='',
                                 blank=True)
    upload_at = models.DateField(default=date.today,
                                 editable=True)
    upload_url = models.FileField(upload_to=directory_path,
                                  default=None,
                                  null=True,
                                  blank=True)
    document = models.ForeignKey('Document',
                                 related_name='document',
                                 on_delete=models.PROTECT,
                                 blank=True,
                                 null=True)
    objects = models.Manager()

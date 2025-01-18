import os
from datetime import date

from django.db.models import Q
from django.db import models
from makemake.projects.models import Project
from makemake.categories.models import Category
from makemake.buildings.models import Building
from makemake.core.custom_functions import left_pad
from makemake.core.choices import FILE_EXTENSION_CHOICES, DOCUMENT_STATUS_CHOICES

class Document(models.Model):
    summary = models.TextField(default='', max_length=100)
    description = models.TextField(default='')
    created_at = models.DateField(default=date.today)
    updated_at = models.DateField(default=date.today)
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
    doctype = models.PositiveSmallIntegerField(null=False, default=None, choices=FILE_EXTENSION_CHOICES,)
    docstatus = models.PositiveSmallIntegerField(null=True, blank=True, default=0, choices=DOCUMENT_STATUS_CHOICES,)
    sequential = models.IntegerField(null=False, default=0,)
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
        numproject = self.document.project.pk
        category_code = self.document.categories.code
        building = self.document.building.number
        numproject = left_pad(numproject)
        building_number = left_pad(building)
        coding = str(self.document.project.year) + str(self.document.project.code)
        path = '{0}/{1}/{2}/{3}'.format(
            building_number,
            coding,
            category_code,
            filename
        )
        return path
    
    released = models.IntegerField(default=1,)
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
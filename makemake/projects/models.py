from django.db import models
from django.contrib.auth.models import User

from datetime import date
from makemake.buildings.models import Building


class Project(models.Model):
    code = models.CharField(max_length=7, default='')
    name = models.CharField(max_length=200, default='',)
    description = models.TextField(default='', blank=True)
    created_at = models.DateField(default=date.today, editable=True)
    updated_at = models.DateField(default=date.today, editable=True)
    buildings = models.ManyToManyField(Building, related_name='buildings', blank=True)
    project_manager = models.ForeignKey(User, related_name='manager', on_delete=models.PROTECT, blank=True, null=True,)
    project_management_support = models.ForeignKey(User, related_name='support', on_delete=models.PROTECT, blank=True, null=True,)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    #project_stakeholders = models.ManyToManyField(User, related_name='stakeholders', blank=True)
    stakeholders = models.ManyToManyField(User, related_name='stakeholders', blank=True)
    interlocutor = models.TextField(default='', blank=True)
    objects = models.Manager()  # The default manager

    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ['created_at', 'name', ]

    def __str__(self):
        return self.name
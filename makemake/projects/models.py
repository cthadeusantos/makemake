from typing import Any
from django.db import models
from django.contrib.auth.models import User

from datetime import date, datetime
from makemake.buildings.models import Building

def ano_corrente():
    return datetime.now().year

class Project(models.Model):
    code = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=ano_corrente)
    name = models.CharField(max_length=200, default='',)
    description = models.TextField(default='', blank=True)
    created_at = models.DateField(default=date.today, editable=True)
    updated_at = models.DateField(default=date.today, editable=True)
    buildings = models.ManyToManyField(Building, related_name='buildings', blank=True)
    project_manager = models.ForeignKey(User, related_name='manager', on_delete=models.PROTECT, blank=True, null=True,)
    project_manager_support = models.ForeignKey(User, related_name='support', on_delete=models.PROTECT, blank=True, null=True,)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    #project_stakeholders = models.ManyToManyField(User, related_name='stakeholders', blank=True)
    stakeholders = models.ManyToManyField(User, related_name='stakeholders', blank=True)
    interlocutor = models.TextField(default='', blank=True)
    objects = models.Manager()  # The default manager

    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ['created_at', 'name', ]
        
        # Define a chave composta para garantir que 'code' e 'year' sejam únicos juntos
        unique_together = ('code', 'year')

    def __str__(self):
        return self.name
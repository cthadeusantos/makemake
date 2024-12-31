from django.db import models
from datetime import date

from makemake.projects.models import Project
from makemake.companies.models import Company

from makemake.core.choices import AGREEMENT_CATEGORIES_CHOICES

class Agreement(models.Model):
    description = models.TextField(default='')
    category = models.PositiveSmallIntegerField(null=False, default=None, choices=AGREEMENT_CATEGORIES_CHOICES,)
    start = models.DateField(default=date.today, editable=True)
    end = models.DateField(default=date.today, editable=True)
    project = models.ForeignKey(Project, related_name='agreeproject', on_delete=models.PROTECT,)
    companies = models.ManyToManyField(Company)

    def __str__(self):
        return self.description
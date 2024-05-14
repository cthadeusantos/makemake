from django.db import models

from django.contrib.auth.models import User

#from makemake.projects.models import Project
#from makemake.companies.models import Company
from makemake.compositions.models import Composition
from makemake.agreements.models import Agreement
from makemake.categories.models import Category

from makemake.core.choices import PLACES_CHOICES, PRICE_TYPE_CHOICES
#from makemake.core.choices import AGREEMENT_CATEGORIES_CHOICES

from datetime import date

class Budget(models.Model):
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0.0, blank=False, null=True,)
    date = models.DateField(default=date.today, editable=True, blank=False, null=True,)
    composition = models.ForeignKey(Composition, blank=False, null=False, on_delete=models.PROTECT,)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=False, null=False,)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False,)
    agreement = models.ForeignKey(Agreement, blank=False, null=False, on_delete=models.CASCADE,)

class PriceLabel(models.Model):
    reference = models.DateField(default=date.today, editable=True, blank=False, null=True,)
    date = models.DateField(default=date.today, editable=True, blank=False, null=True,)
    label = models.TextField(default="")
    discontinued = models.BooleanField(blank=True, default=False,)
    
    def __str__(self):
        return self.label

class Price(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=False, null=True,)
    date = models.DateField(default=date.today, editable=True, blank=False, null=True,)
    burdened = models.BooleanField(blank=True,default=False, choices=PRICE_TYPE_CHOICES,)
    place = models.PositiveSmallIntegerField(default=0,choices=PLACES_CHOICES)
    label = models.ForeignKey(PriceLabel, blank=False, null=False, on_delete=models.PROTECT,)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False,)
    composition = models.ForeignKey(Composition, on_delete=models.PROTECT, blank=False, null=True,)

class CompositionHasPrice(models.Model):
    date = models.DateField(default=date.today, editable=True, blank=False, null=True,)
    budget = models.ForeignKey(Budget, on_delete=models.PROTECT, blank=False, null=True,)
    price = models.ForeignKey(Price, on_delete=models.PROTECT, blank=False, null=True,)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, blank=False, null=False,)

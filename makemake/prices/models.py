from django.db import models

from datetime import date

from makemake.core.choices import PRICE_TYPE_CHOICES, PLACES_CHOICES

from django.contrib.auth.models import User
from makemake.compositions.models import Composition

class PriceLabel(models.Model):
    reference = models.DateField(default=date.today, editable=True, blank=False, null=True,)
    date = models.DateField(default=date.today, editable=True, blank=False, null=True,)
    name = models.TextField(default="", unique=False)
    discontinued = models.BooleanField(blank=True, default=False,)

    def __str__(self) -> str:
        return self.name

class Price(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=False, null=True,)
    date = models.DateField(default=date.today, editable=True, blank=False, null=True,)
    burdened = models.BooleanField(blank=True,default=False, choices=PRICE_TYPE_CHOICES,)
    place = models.PositiveSmallIntegerField(default=0,choices=PLACES_CHOICES)
    label = models.ForeignKey(PriceLabel, blank=False, null=False, on_delete=models.PROTECT,)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False,)
    composition = models.ForeignKey(Composition, on_delete=models.PROTECT, blank=False, null=True,)

class PriceTemp(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=False, null=True,)
    date = models.DateField(default=date.today, editable=True, blank=False, null=True,)
    burdened = models.BooleanField(blank=True,default=False, choices=PRICE_TYPE_CHOICES,)
    place = models.PositiveSmallIntegerField(default=0,choices=PLACES_CHOICES)
    label = models.ForeignKey(PriceLabel, blank=False, null=False, on_delete=models.PROTECT,)
    #user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False,)
    composition = models.ForeignKey(Composition, on_delete=models.PROTECT, blank=False, null=True,)

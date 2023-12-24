from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from makemake.core.choices import BUILDING_STATUS_CHOICES
#from makemake.projects.models import Project
from makemake.sites.models import Site

class Building(models.Model):
    name = models.CharField(blank=False,
                            null=False,
                            default="",
                            max_length=200,)

    number = models.PositiveSmallIntegerField(default=0,
                                              null=False,
                                              blank=False,
                                              validators=[MinValueValidator(0), MaxValueValidator(32767)],
                                              unique=True,
                                              )
    status = models.PositiveSmallIntegerField(choices=BUILDING_STATUS_CHOICES,
                                              null=False,
                                              blank=False,
                                              )
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=False, blank=False, default=None)
    created_at = models.DateField(default=date.today, editable=True)
    updated_at = models.DateField(default=date.today, editable=True)
    objects = models.Manager()  # The default manager

    def __str__(self):
        return self.name

from django.db import models

from makemake.core.choices import UNIT_CHOICES

from datetime import datetime

class Unit(models.Model):
    name = models.CharField(max_length=45,
                            # unique=True,
                            default="",)
    symbol = models.CharField\
        (
            max_length=10,
            null=False,
            blank=False,
            unique=True,
            default="",
        )
    symbol_alternative1 = models.CharField\
        (
            max_length=10,
            null=False,
            blank=False,
            unique=True,
            default="",
        )
    symbol_alternative2 = models.CharField\
        (
            max_length=10,
            null=False,
            blank=False,
            unique=True,
            default="",
        )
    type = models.PositiveSmallIntegerField\
        (
            choices=UNIT_CHOICES,
            default=0,
            null=False,
            blank=False,
        )
    #objects = models.Manager()
    #managers = UnitManager()

    # # Change save method to modify specific fields to uppercase
    # def save(self, *args, **kwargs):
    #     try:
    #         self.name = self.name.capitalize()
    #     except:
    #         self.name = 'UNAMED_' + datetime.now().strftime("%m%d%Y%H%M%S")
    #     return super(Unit, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
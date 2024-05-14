from django.db import models
from datetime import datetime

from makemake.units.models import Unit

from makemake.core.choices import BUDGETS_DATABASES_CHOICES, TYPE_COMPOSITION_CHOICES, ORIGIN_PRICES_CHOICES, PRICES_DATABASES_CHOICES

class Composition(models.Model):
    code = models.CharField(
        blank=False,
        null=False,
        #unique=True,
        max_length=20,
        default="",
        )
    description = models.TextField(
        blank=False,
        null=False,
        default=""
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        )
    type = models.IntegerField(
            choices=TYPE_COMPOSITION_CHOICES,
            default=0,
            null=False,
            blank=False,
        )
    iscomposition = models.BooleanField(
        blank=True,
        #null=True,
        default=False,
        )
    dbtype = models.PositiveSmallIntegerField(
        default=0,
        choices=BUDGETS_DATABASES_CHOICES,
        )
    discontinued = models.BooleanField(
        blank=True,
        #null=True,
        default=False,
        )
    created_at = models.DateField(
        default=datetime.now,
        blank=True,
        )
    updated_at = models.DateField(
        default=datetime.now,
        blank=True,
        )

    #categories = models.ManyToManyField(Category)
    compositions = models.ManyToManyField('Composition', through="CompositionHasComponents", related_name="comps")
    objects = models.Manager()  # The default manager
    #managers = CompositionManager()  # My custom manager
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'dbtype'], name='unique_code_table')
        ]

    def __str__(self):
        return self.description

class CompositionHasComponents(models.Model):
    composition_master = models\
        .ForeignKey(Composition,
                    on_delete=models.CASCADE,
                    related_name='master',)
    composition_slave = models\
        .ForeignKey(Composition,
                    on_delete=models.PROTECT,
                    related_name='slave',)
    # add_date = models.DateField(default=datetime.now)
    origin = models.SmallIntegerField(
        blank=True,
        null=True,
        default=1,
        choices=ORIGIN_PRICES_CHOICES,
    )
    quantity = models\
        .DecimalField(max_digits=12,
                      decimal_places=7,
                      default=0)
    dbprices = models.PositiveSmallIntegerField(
        default=0,
        choices=PRICES_DATABASES_CHOICES,
        )
    #objects = models.Manager()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['composition_master', 'composition_slave'], name='unique_code_table_hascomponent')
        ]

    def __str__(self) -> str:
        return self.composition_slave.description

class PriceIndex(models.Model):
    code = models.ForeignKey(Composition,
                             related_name='item_prices',
                             on_delete=models.PROTECT,
                             blank=False,
                             null=False,)
    price = models\
        .DecimalField(max_digits=10,
                      decimal_places=2,
                      default=0.00)
    collectiont_date = models.DateField(
        default=datetime.now,
        blank=True,
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'collectiont_date'], name='unique_code_collectiont_date')
        ]

    def __str__(self) -> str:
        return f"{self.composition_slave.description}: {str(self.price)}"

def composition_can_be_deleted(self):
    # Implement logic to check if the register can be deleted
    return True

def composition_can_be_updated(self):
    # Implement logic to check if the register can be updated
    return True
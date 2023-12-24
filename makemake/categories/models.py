from django.db import models
from datetime import date


class Category(models.Model):
    code = models.CharField(max_length=3, default='',)
    name = models.CharField(max_length=50, default='',)
    description = models.TextField(default='', blank=True)
    #created_at = models.DateField(default=date.today, editable=True)
    #updated_at = models.DateField(default=date.today, editable=True)
    category = models.ForeignKey('self', related_name='relcategory', blank=True, null=True, on_delete=models.PROTECT)
    objects = models.Manager()  # The default manager

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name', 'code', ]

    def __str__(self):
        return self.name
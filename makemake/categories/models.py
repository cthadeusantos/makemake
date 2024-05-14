from django.db import models
from datetime import date

class Category(models.Model):
    code = models.CharField(max_length=3, default='', unique=True)
    name = models.CharField(max_length=50, default='',)
    description = models.TextField(default='', blank=True)
    parents = models.ManyToManyField('self', blank=True, symmetrical=False)
    fordocs = models.BooleanField(default=True)
    forbudgets = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name', 'code', ]

    def __str__(self):
        return self.name
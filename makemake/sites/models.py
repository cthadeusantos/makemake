from django.db import models
from makemake.core.choices import CITIES_CHOICES


class Site(models.Model):
    name = models.CharField(max_length=100,
                            default='')
    place = models.PositiveSmallIntegerField(
        default=0,
        choices=CITIES_CHOICES)

    objects = models.Manager()  # The default manager

    class Meta:
        verbose_name_plural = 'Sites'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name[:1].upper() + self.name[1:]
        return super(Site, self).save(*args, **kwargs)
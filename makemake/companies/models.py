from django.db import models

class Company(models.Model):
    name = models.TextField(default='')
    number = models.CharField(max_length=14, default='')
from makemake.projects.models import Project  

#from auditlog.middleware import get_actor

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from auditlog.models import LogEntry
from auditlog.registry import auditlog
from django.contrib.contenttypes.models import ContentType



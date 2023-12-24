from django.forms import ModelForm

from makemake.sites.models import Site
from makemake.buildings.models import Building


class SiteForm(ModelForm):
    class Meta:
        model = Site
        fields = [
            'name',
            'place',
        ]
        labels = {
            'name': 'Site',
            'place': 'Place',
        }
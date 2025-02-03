from django.apps import AppConfig


class SitesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'makemake.sites'

    # def ready(self):
    #     import makemake.sites.signals  # Certifique-se de ajustar o caminho

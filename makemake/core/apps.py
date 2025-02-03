from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'makemake.core'
    
    def ready(self):
        import makemake.core.signals
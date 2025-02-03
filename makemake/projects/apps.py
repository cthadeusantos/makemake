from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'makemake.projects'

    def ready(self):
        import makemake.projects.signals  # Certifique-se de ajustar o caminho

from django.apps import AppConfig


class PlantelesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'planteles'

    def ready(self):
        import planteles.signals
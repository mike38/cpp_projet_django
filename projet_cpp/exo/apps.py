from django.apps import AppConfig


class ExoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exo'

    # def ready(self):
    # 	import exo.signals
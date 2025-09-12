from django.apps import AppConfig


class DocMgrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'docmgr'
    verbose_name = 'Document Manager'

    def ready(self):
        import docmgr.signals

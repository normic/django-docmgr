from django.apps import AppConfig


class DocMgrConfig(AppConfig):
    name = 'docmgr'
    verbose_name = 'Document Manager'

    def ready(self):
        import docmgr.signals

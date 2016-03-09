from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Document


@receiver(post_delete, sender=Document)
def model_post_delete(sender, instance, **kwargs):
    storage, path = instance.docfile.storage, instance.docfile.path
    storage.delete(path)

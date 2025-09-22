from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Document


@receiver(post_delete, sender=Document)
def model_post_delete(sender, instance, **kwargs):
    """
        Removes the corresponding file from the storage
    """

    try:
        storage, name = instance.docfile.storage, instance.docfile.name
    except ValueError:
        """
            ValueError os thrown if there is no file to delete
            We simply ignore it, cause we nevertheless want to delete it
        """
        pass

    storage.delete(name)


@receiver(pre_save, sender=Document)
def model_pre_save(sender, instance, **kwargs):
    """
        Removes file from storage when the corresponding file object is changed
    """
    if not instance.pk:
        return False

    try:
        old_file = Document.objects.get(pk=instance.pk).docfile
    except Document.DoesNotExist:
        return False

    new_file = instance.docfile

    if not old_file == new_file:
        storage, name = old_file.storage, old_file.name
        storage.delete(name)

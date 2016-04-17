import time
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .app_settings import UPLOAD_PATH

docstorage = FileSystemStorage(location=UPLOAD_PATH)


def get_upload_path(instance, filename):
    return "{structure}/{file}".format(structure=time.strftime('%Y'), file=filename)


class Document(models.Model):
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4, editable=False)
    docfile = models.FileField(
        upload_to=get_upload_path,
        storage=docstorage,
        help_text=_('Click on fieldname or image to open the upload dialog.')
    )
    description = models.TextField(
        _('Description'),
        help_text=_('An optional description of the file.'),
        blank=True
    )
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    uploaded_at = models.DateTimeField(default=timezone.now, editable=False)

    def filename(self):
        return self.docfile.name

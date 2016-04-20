import os
import time
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .app_settings import UPLOAD_PATH

docstorage = FileSystemStorage(location=UPLOAD_PATH)


def get_upload_path(instance, filename):
    """
    cleans filename and returns the current year and
    the cleaned filename as upload location
    """
    fname, dot, extension = filename.rpartition('.')
    slugged_filename = slugify(fname)
    slugged = '%s.%s' % (slugged_filename, extension)
    return "{structure}/{file}".format(structure=time.strftime('%Y'), file=slugged)


class Document(models.Model):
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4, editable=False)
    docfile = models.FileField(
        _('Document File'),
        upload_to=get_upload_path,
        storage=docstorage,
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

    @property
    def filepath(self):
        """
        returns the structured path with the filename
        defaults to <currentyear>/<slugifiedfilename>
        """
        return self.docfile.name

    @property
    def filename(self):
        """ returns the (slugified) filename only """
        return os.path.basename(self.docfile.name)

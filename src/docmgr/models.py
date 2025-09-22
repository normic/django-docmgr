import os
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .app_settings import UPLOAD_PATH, UPLOAD_STRUCTURE

docstorage = FileSystemStorage(location=UPLOAD_PATH)


def get_upload_path(instance, filename):
    """
    Cleans filename and returns the upload location according to configuration.
    Default: <currentyear>/<slugifiedfilename>
    Supported structures via settings.DOCMGR_UPLOAD_STRUCTURE:
      - "year": YYYY/
      - "year_month": YYYY/MM/
      - "date" or "date_iso": YYYY-MM-DD/
    """
    # Split filename into name and extension (if any)
    fname, dot, extension = filename.rpartition(".")
    base = fname if fname else filename  # when no dot present, rpartition returns ('', '', filename)
    slugged_filename = slugify(base)
    if extension:
        slugged = f"{slugged_filename}.{extension}"
    else:
        slugged = slugged_filename

    structure_key = str(UPLOAD_STRUCTURE).lower() if UPLOAD_STRUCTURE is not None else "year"
    now = timezone.now()

    if structure_key == "year_month":
        structure = now.strftime("%Y/%m")
    elif structure_key in ("date", "date_iso"):
        # ISO 8601 date format
        structure = now.strftime("%Y-%m-%d")
    else:
        # default and fallback
        structure = now.strftime("%Y")

    return f"{structure}/{slugged}"


class Document(models.Model):
    # Explicit default manager to satisfy static analyzers (e.g., PyCharm, pylint)
    objects = models.Manager()

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    docfile = models.FileField(
        _("Document File"),
        upload_to=get_upload_path,
        storage=docstorage,
    )
    description = models.TextField(
        _("Description"),
        help_text=_("An optional description of the file."),
        blank=True,
    )
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.SET_NULL)
    object_id = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

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
        """returns the (slugified) filename only"""
        return os.path.basename(self.docfile.name)

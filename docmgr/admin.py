from django.contrib import admin
from django.contrib.contenttypes.admin import (
    GenericStackedInline,
    GenericTabularInline
)
from django.core.files.storage import FileSystemStorage
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Document
from .forms import DocumentAdminForm

storage = FileSystemStorage()


class DocumentStackedInline(GenericStackedInline):
    form = DocumentAdminForm
    model = Document
    extra = 0
    readonly_fields = ['filename', ]


class DocumentTabularInline(GenericTabularInline):
    form = DocumentAdminForm
    model = Document
    extra = 0
    readonly_fields = ['filename', ]


class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ['pk', 'filepath', 'description', 'content_type', 'object_id', 'preview_image']

    def preview_image(self, obj):
        return format_html(
            '<img src="/docmgr/default-file/%s" style="max-width: 180px; max-height: 150px;" />' % (obj.pk)
        )
    preview_image.short_description = _(u'Featured Image')


admin.site.register(Document, DocumentAdmin)

# coding: utf-8

from django.contrib import admin
from django.contrib.contenttypes.admin import (
    GenericStackedInline,
    GenericTabularInline
)
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Document
from .forms import DocumentAdminForm


class DocumentStackedInline(GenericStackedInline):
    form = DocumentAdminForm
    model = Document
    extra = 1


class DocumentTabularInline(GenericTabularInline):
    form = DocumentAdminForm
    model = Document
    extra = 1


class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ['pk', 'docfile', 'description', 'content_type', 'object_id', 'featured_image']

    def featured_image(self, obj):
        return format_html(
            '<img src="%s" style="max-width: 180px; max-height: 150px;" />' % (obj.docfile.url)
        )
    featured_image.short_description = _(u'Featured Image')


admin.site.register(Document, DocumentAdmin)

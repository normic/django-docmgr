from django import template
from django.conf import settings

from docmgr.models import Document

register = template.Library()


# debug: uuid '27851dd9-ec22-4a34-acac-1b3122fd4c6c'
@register.inclusion_tag('docmgr/_featured_image.html')
def featured_image(uuid_document, maxwidth='180px', maxheight='150px'):
    try:
        previewdoc = Document.objects.get(pk=uuid_document)
        previewurl = settings.MEDIA_URL + str(previewdoc)
        return {
            'maxwidth': maxwidth,
            'maxheight': maxheight,
            'previewdoc': previewdoc,
            'previewurl': previewurl
        }
    except Document.DoesNotExist:
        return {}

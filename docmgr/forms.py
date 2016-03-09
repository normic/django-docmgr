from django.forms import ModelForm

from .models import Document
from .widgets import DocumentPreviewWidget


class DocumentAdminForm(ModelForm):
    class Meta(object):
        model = Document
        fields = '__all__'

        widgets = {
            'docfile': DocumentPreviewWidget(),
        }

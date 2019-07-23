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

    def __init__(self, *args, **kwargs):
        super(DocumentAdminForm, self).__init__(*args, **kwargs)

        try:
            self.fields['docfile'].widget.form_instance = self
        except KeyError:
            pass

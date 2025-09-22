from django.forms.widgets import ClearableFileInput
from django.utils.html import conditional_escape


class DocumentPreviewWidget(ClearableFileInput):
    """
        A Filefield Widget which shows a clickable image if it has a value
        If the value is an image it shows a preview otherwise a thumbnail
        indicating it's a document
    """
    template_name = 'clearable_file_input.html'

    INPUT_CLASS = 'document-preview'

    def __init__(self, attrs=None):
        super(DocumentPreviewWidget, self).__init__(attrs)
        self.attrs['class'] = self.INPUT_CLASS

    def get_context(self, name, value, attrs):
        context = super(DocumentPreviewWidget, self).get_context(name, value, attrs)
        checkbox_name = self.clear_checkbox_name(name)
        checkbox_id = self.clear_checkbox_id(checkbox_name)

        img_src = ''
        img_width = 'width=100px'

        # check if filename is set
        if value:
            # TODO: make path configurable (not only in urls.py)
            doc_src = '/docmgr/default-file/' + conditional_escape(self.form_instance.instance.pk)

            if value.name.endswith(('.jpg', '.gif', '.tif', '.png')):
                img_src = doc_src
            else:
                img_src = '/static/images/_blank.png'
                img_width = 'width=48px'
        else:
            doc_src = value

        context.update({
            'checkbox_name': checkbox_name,
            'checkbox_id': checkbox_id,
            'is_initial': self.is_initial(value),
            'input_text': self.input_text,
            'initial_text': self.initial_text,
            'clear_checkbox_label': self.clear_checkbox_label,
            'doc_src': doc_src,
            'img_src': img_src,
            'img_width': img_width,
        })
        return context

    class Media(object):
        css = {
            'all': ('css/document_preview_widget.css',)
        }

from django.conf import settings
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


class DocumentPreviewWidget(ClearableFileInput):

    class Media(object):
        css = {
            'all': ('css/document_preview_widget.css',)
        }
        js = ('js/document_preview_widget.js', )  # pylint: disable=C0103

    template_with_initial = (
        '<label for=%(id_for_label)s> \
        <img id="%(img_id)s" src="' +
        settings.MEDIA_URL + '%(initial)s" width="100px"> \
        </label>'
        '%(clear_template)s<br />%(input)s'
    )

    INPUT_CLASS = 'document-preview'

    def __init__(self, attrs=None):
        super(DocumentPreviewWidget, self).__init__(attrs)
        self.attrs['class'] = self.INPUT_CLASS

    def render(self, name, value, attrs=None):
        id_for_label = self.id_for_label(attrs.get('id'))

        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
            'id_for_label': id_for_label,
            'img_id': id_for_label + '_img',
        }
        template = '%(input)s'
        substitutions['input'] = Input.render(self, name, value, attrs)

        if self.is_initial(value):
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(
                    checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(
                    checkbox_id)
                substitutions['clear'] = CheckboxInput().render(
                    checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = \
                    self.template_with_clear % substitutions

        return mark_safe(template % substitutions)


class DropzoneFileUpload(ClearableFileInput):

    class Media(object):
        css = {
            'all': ('css/basic.min.css', 'css/dropzone.min.css')
        }
        js = ('js/dropzone-amd-module.min.js', 'js/dropzone.min.js')

    template_with_initial = (
        '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
        '%(clear_template)s<br />%(input_text)s: %(input)s'
    )

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        #substitutions['input'] = super(DropzoneFileUpload, self).render(
        #    name, value, attrs)
        #print dir(self)
        #print vars(self)
        #self.attrs = {'class="dropzone"'}
        output = super(DropzoneFileUpload, self).render(name, value, attrs)

        output = output.replace('type="file"', 'type="file" class="dropzone"')
        print output
        #print template
        #print substitutions
        return mark_safe(output)

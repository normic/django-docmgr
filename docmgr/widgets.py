from django.forms.widgets import ClearableFileInput, Input, CheckboxInput
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


class DocumentPreviewWidget(ClearableFileInput):
    """
        A Filefield Widget which shows a clickable image if it has a value
        If the value is an image it shows a preview otherwise a thumbnail
        indicating it's a document
    """

    # The "for" in the <label> allows to open the "open file" dialog by
    # clicking on the image, no js involved
    # template_with_initial = (
    #     '<label for=%(id_for_label)s> <img id="%(img_id)s" \
    #         src="%(img_src)s" %(img_width)s> </label>'
    #     '%(clear_template)s<br />%(input)s'
    # )
    template_with_initial = (
        '<a href="%(doc_src)s" target="_blank"><img id="%(img_id)s" src="%(img_src)s" %(img_width)s class="img-thumbnail document-preview"></a>'
        '%(clear_template)s<br />%(input)s'
    )

    INPUT_CLASS = 'document-preview'

    def __init__(self, attrs=None):
        super(DocumentPreviewWidget, self).__init__(attrs)
        self.attrs['class'] = self.INPUT_CLASS

    def render(self, name, value, attrs=None):
        # quick'n dirty hack to differentiate between filetypes by extension
        doc_src = ''
        img_src = ''
        img_width = 'width="100px"'

        if value:
            doc_src = '/docmgr/default-file/' + conditional_escape(self.form_instance.instance.pk)
            if value.name.endswith(('.jpg', '.gif', '.tif', '.png')):
                img_src = doc_src
            else:
                img_src = '/static/images/_blank.png'
                img_width = 'width="48px"'

        id_for_label = self.id_for_label(attrs.get('id'))
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
            'id_for_label': id_for_label,
            'img_id': id_for_label + '_img',
            'doc_src': doc_src,
            'img_src': img_src,
            'img_width': img_width,
        }
        template = '%(input)s'
        substitutions['input'] = Input.render(self, name, value, attrs)

        if self.is_initial(value):
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

    class Media(object):
        css = {
            'all': ('css/document_preview_widget.css',)
        }
        js = ('js/document_preview_widget.js', )

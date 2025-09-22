from braces.views import (
    LoginRequiredMixin,
    AjaxResponseMixin,
    JSONResponseMixin
)
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.generic import View
from django_downloadview import ObjectDownloadView, StorageDownloadView

from .app_settings import UPLOAD_PATH
from .forms import DocumentAdminForm
from .models import Document

storage = FileSystemStorage(location=UPLOAD_PATH)

default_file_view = ObjectDownloadView.as_view(
    model=Document,
    file_field='docfile',
    attachment=False
)


class DocumentThumbnailView(LoginRequiredMixin, StorageDownloadView):

    def get_path(self):
        return super(DocumentThumbnailView, self).get_path()


dynamic_path = DocumentThumbnailView.as_view(storage=storage, attachment=False)


class DocumentUploadView(LoginRequiredMixin,
                         JSONResponseMixin, AjaxResponseMixin, View):
    form_class = DocumentAdminForm
    template_name = 'document_uploader.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post_ajax(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']

        Document.objects.create(
            docfile=uploaded_file,
            description=''
        )

        response_dict = {
            'message': 'File(s) successfully uploaded.',
        }
        return self.render_json_response(response_dict, status=200)

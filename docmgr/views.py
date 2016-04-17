from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.generic import View

from braces.views import (
    LoginRequiredMixin,
    AjaxResponseMixin,
    JSONResponseMixin
)
from django_downloadview import ObjectDownloadView, StorageDownloadView

from .models import Document
from .forms import DocumentAdminForm

storage = FileSystemStorage()


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

    """
    def dispatch(self, *args, **kwargs):
        return super(DocumentUploadView, self).dispatch(*args, **kwargs)
    """

    def post_ajax(self, request, *args, **kwargs):
        """
        try:
            folder = Folder.objects.get(pk=kwargs.get('pk'))
        except Folder.DoesNotExist:
            error_dict = {'message': 'Requested Folder not found.'}
            return self.render_json_response(error_dict, status=404)
        """

        uploaded_file = request.FILES['file']

        Document.objects.create(
            docfile=uploaded_file,
            description=''
        )

        response_dict = {
            'message': 'File(s) successfully uploaded.',
        }
        return self.render_json_response(response_dict, status=200)

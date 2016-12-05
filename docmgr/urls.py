from django.conf.urls import url
from django.contrib.auth.decorators import permission_required

from .views import (
    DocumentUploadView,
    dynamic_path,
    default_file_view,
)


urlpatterns = [
    url(
        r'^doc-upload/$',
        view=DocumentUploadView.as_view(),
        name='document_upload_view',
    ),
    url(
        r'^(?P<path>[a-zA-Z0-9_-]+\.[a-zA-Z0-9]{1,4})$',
        dynamic_path,
        name='dynamic_path'
    ),
    url(
        r'^default-file/(?P<pk>[a-zA-Z0-9_-]+)/$',
        permission_required('docmgr.change_document')(default_file_view),
        name='default_file'
    ),
]

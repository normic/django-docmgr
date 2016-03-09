from django.conf.urls import url

from .views import DocumentUploadView

# pylint: disable=C0103
urlpatterns = [
    url(
        r'^doc-upload/$',
        view=DocumentUploadView.as_view(),
        name='document_upload_view',
    ),
]

"""
    # we may use this if we want to put a file in a folder
    url(
        regex=r'^doc-upload/(?P<pk>\d+)/$',
        view=views.DocumentUploadView.as_view(),
        name='document_upload_view',
    ),
"""

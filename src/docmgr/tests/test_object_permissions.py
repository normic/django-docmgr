from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from docmgr.drf import DocumentViewSet
from docmgr.models import Document


class MockObjectPermissionHandler:
    def has_object_permission(self, user, obj, action):
        # Only allow access if the user has a specific attribute or if we say so
        if getattr(user, 'allow_doc_access', False):
            return True
        return False

    def filter_queryset(self, user, queryset):
        if getattr(user, 'allow_doc_access', False):
            return queryset
        return queryset.none()

class ObjectPermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="testuser", password="password")
        # Give user basic model permissions for Document
        content_type = ContentType.objects.get_for_model(Document)
        view_perm = Permission.objects.get(content_type=content_type, codename="view_document")
        self.user.user_permissions.add(view_perm)
        
        self.doc = Document.objects.create(
            docfile=SimpleUploadedFile("test.txt", b"content"),
            description="test doc"
        )
        self.view = DocumentViewSet.as_view({'get': 'retrieve'})
        self.list_view = DocumentViewSet.as_view({'get': 'list'})

    @override_settings(DOCMGR_OBJECT_PERMISSION_HANDLER='docmgr.tests.test_object_permissions.MockObjectPermissionHandler')
    def test_object_permission_denied(self):
        self.user.allow_doc_access = False
        request = self.factory.get(f'/api/documents/{self.doc.uuid}/')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=str(self.doc.uuid))
        # It's 404 because filter_queryset removes it
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @override_settings(DOCMGR_OBJECT_PERMISSION_HANDLER='docmgr.tests.test_object_permissions.MockObjectPermissionHandler')
    def test_object_permission_allowed(self):
        self.user.allow_doc_access = True
        request = self.factory.get(f'/api/documents/{self.doc.uuid}/')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=str(self.doc.uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(DOCMGR_OBJECT_PERMISSION_HANDLER='docmgr.tests.test_object_permissions.MockObjectPermissionHandler')
    def test_filter_queryset_denied(self):
        self.user.allow_doc_access = False
        request = self.factory.get('/api/documents/')
        force_authenticate(request, user=self.user)
        response = self.list_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results'] if 'results' in response.data else response.data), 0)

    @override_settings(DOCMGR_OBJECT_PERMISSION_HANDLER='docmgr.tests.test_object_permissions.MockObjectPermissionHandler')
    def test_filter_queryset_allowed(self):
        self.user.allow_doc_access = True
        request = self.factory.get('/api/documents/')
        force_authenticate(request, user=self.user)
        response = self.list_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)

import os
import io
from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser, User
from django.template.defaultfilters import slugify
from django.test import RequestFactory, TestCase
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile

from docmgr.models import get_upload_path, Document
from docmgr import views as doc_views


class UploadPathTests(TestCase):
    def test_year_structure_and_slugging(self):
        with patch("docmgr.models.timezone.now", return_value=datetime(2025, 9, 18, 12, 0, 0)):
            with patch("docmgr.models.UPLOAD_STRUCTURE", "year"):
                result = get_upload_path(None, "Dää gegen.jpg")
                # Expect '2025/<slug>.jpg'
                self.assertTrue(result.startswith("2025/"))
                base = "Dää gegen"  # without extension
                expected_slug = slugify(base)
                self.assertTrue(result.endswith(".jpg"))
                self.assertIn(expected_slug + ".jpg", result)

    def test_year_month_and_date_structures(self):
        with patch("docmgr.models.timezone.now", return_value=datetime(2025, 1, 5, 8, 0, 0)):
            with patch("docmgr.models.UPLOAD_STRUCTURE", "year_month"):
                p = get_upload_path(None, "Report.pdf")
                self.assertTrue(p.startswith("2025/01/"))
            with patch("docmgr.models.UPLOAD_STRUCTURE", "date"):
                p = get_upload_path(None, "Report.pdf")
                self.assertTrue(p.startswith("2025-01-05/"))


class DynamicPathSecurityTests(TestCase):
    def setUp(self):
        # Ensure upload directory exists and create a small test file there
        self.upload_root = doc_views.UPLOAD_PATH
        os.makedirs(self.upload_root, exist_ok=True)
        self.filename = "example.txt"
        self.filepath = os.path.join(self.upload_root, self.filename)
        with open(self.filepath, "wb") as f:
            f.write(b"hello world")
        self.factory = RequestFactory()

    def tearDown(self):
        try:
            os.remove(self.filepath)
        except FileNotFoundError:
            pass

    def test_storage_points_to_upload_path(self):
        # The download storage must be bound to UPLOAD_PATH (not MEDIA_ROOT)
        self.assertEqual(doc_views.storage.base_location, doc_views.UPLOAD_PATH)

    def test_login_required_redirects_anonymous(self):
        request = self.factory.get(f"/docmgr/{self.filename}")
        request.user = AnonymousUser()
        response = doc_views.dynamic_path(request, path=self.filename)
        # LoginRequiredMixin redirects anonymous users (302)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_download_existing_file(self):
        user = User.objects.create_user(username="alice", password="secret")
        request = self.factory.get(f"/docmgr/{self.filename}")
        request.user = user
        response = doc_views.dynamic_path(request, path=self.filename)
        self.assertEqual(response.status_code, 200)
        # Read a bit of the streaming response to ensure content
        chunk = next(response.streaming_content)
        self.assertIn(b"hello", chunk)

import os
from io import BytesIO

import pytest
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from docmgr.models import Document, docstorage


class SignalReceiverTests(TestCase):
    def setUp(self):
        # Ensure storage base location exists
        os.makedirs(docstorage.base_location, exist_ok=True)

    def _create_document_with_content(self, name="sample.txt", content=b"hello"):
        # Use SimpleUploadedFile to simulate an upload to storage
        uploaded = SimpleUploadedFile(name, content)
        doc = Document.objects.create(docfile=uploaded)
        # Ensure file actually exists on disk
        self.assertTrue(docstorage.exists(doc.docfile.name))
        return doc

    def test_post_delete_removes_file_from_storage(self):
        doc = self._create_document_with_content(name="delete_me.txt", content=b"bye")
        path = doc.docfile.name
        # Sanity check file exists
        self.assertTrue(docstorage.exists(path))
        # Delete model -> post_delete should remove file
        doc.delete()
        self.assertFalse(docstorage.exists(path))

    def test_pre_save_removes_old_file_when_replacing(self):
        doc = self._create_document_with_content(name="first.txt", content=b"first")
        old_path = doc.docfile.name
        # Assign a new file and save -> pre_save should remove old file
        new_upload = SimpleUploadedFile("second.txt", b"second")
        doc.docfile = new_upload
        doc.save()
        # Old file should be removed
        self.assertFalse(docstorage.exists(old_path))
        # New file should exist
        self.assertTrue(docstorage.exists(doc.docfile.name))

    def test_pre_save_no_delete_when_new_instance_without_pk(self):
        # Creating a new instance should not attempt to delete anything
        new_upload = SimpleUploadedFile("new.txt", b"new")
        doc = Document(docfile=new_upload)
        # At this point there's no pk, saving should not try to delete missing old file
        doc.save()  # should not raise and should store the file
        self.assertTrue(docstorage.exists(doc.docfile.name))

    def test_post_delete_handles_missing_file_gracefully(self):
        doc = self._create_document_with_content(name="missing.txt", content=b"x")
        path = doc.docfile.name
        # Manually remove file from storage first
        docstorage.delete(path)
        self.assertFalse(docstorage.exists(path))
        # Now delete model — signal should not crash even though file is already gone
        doc.delete()
        # Nothing to assert beyond absence and absence of exceptions; ensure no file resurrected
        self.assertFalse(docstorage.exists(path))

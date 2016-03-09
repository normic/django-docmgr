from django.test import TestCase


# pylint: disable=E1103
class DocMgrAdminTest(TestCase):
    def test_adminindex(self):
        response = self.client.get('/admin/docmgr/')
        self.assertIn(response.status_code, [200, 302])

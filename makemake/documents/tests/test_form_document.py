from datetime import datetime

from django.test import TestCase
from makemake.documents.forms import DocumentForm


class DocumentFormTest(TestCase):
    def setUp(self):
        self.response_new = self.client.get('/documents/new/')

    def test_has_form(self):
        """Context must have document FORM"""
        form = self.response_new.context['form']
        self.assertIsInstance(form, DocumentForm)

    def test_has_fields(self):
        """FORM must have 4 fields"""
        form = self.response_new.context['form']
        self.assertSequenceEqual(['summary', 'description', 'created_at', 'updated_at'],
                                 list(form.fields))


class DocumentPostTest(TestCase):

    def setUp(self):
        self.data = dict(summary='Projeto 1 - summary',
                    description='Projeto 1- description',
                    created_at=datetime.today(),
                    updated_at=datetime.today())
        self.response = self.client.post('/documents/new/', self.data)

    def test_post(self):
        """Valid POST should redirect to /documents/new/"""
        self.assertEqual(302, self.response.status_code)


class DocumentInvalidPost(TestCase):
    def setUp(self):
        self.response_new = self.client.post('/documents/new/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response_new.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response_new, 'documents/new.html')
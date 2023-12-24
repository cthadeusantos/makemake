from datetime import datetime

from django.test import TestCase
from makemake.documents.models import Document, Version


class DocumentModelTest(TestCase):
    def setUp(self):
        self.obj = Document(
            summary="Projeto 1",
            description="PROJETO 1",
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Document.objects.exists())

    def test_created_at(self):
        self.assertEqual(self.obj.created_at, datetime.today().date())

    def test_updated_at(self):
        self.assertEqual(self.obj.updated_at, datetime.today().date())


class VersionModelTest(TestCase):
    def setUp(self):
        self.obj = Version(
            version_number=1,
            changelog="Adição inicial",
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Version.objects.exists())

    def test_upload_at(self):
        self.assertEqual(self.obj.upload_at, datetime.today().date())
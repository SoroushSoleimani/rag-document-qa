from django.test import TestCase
from .models import Document

class DocumentModelTest(TestCase):
    def setUp(self):
        """
        Set up a temporary environment before running the tests.
        This creates a mock document in an isolated test database.
        """
        self.document = Document.objects.create(
            title="Automated Test Document"
            # We intentionally leave the 'file' blank to test the core logic
            # without triggering the heavy Celery/RAG background tasks.
        )

    def test_document_default_status(self):
        """
        Ensure that a newly created document is assigned the 'pending' 
        status by default before any processing starts.
        """
        self.assertEqual(self.document.status, 'pending')

    def test_document_string_representation(self):
        """
        Test if the Django admin will display the correct name for the document.
        """
        self.assertEqual(str(self.document), "Automated Test Document")
from celery import shared_task
from .models import Document
from .rag_service import RAGService
import os

@shared_task
def process_document_task(document_id):
    """
    Background task to process a document, vectorize it, 
    and dynamically update its processing status in the database.
    """
    try:
        # 1. Fetch the document and update status to 'processing'
        doc = Document.objects.get(id=document_id)
        doc.status = 'processing'
        doc.save()

        # 2. Perform the heavy vectorization task
        file_path = doc.file.path
        rag_service = RAGService()
        rag_service.process_document(file_path)
        
        # 3. Update status to 'completed' upon success
        doc.status = 'completed'
        doc.save()
        
        return f"Successfully processed document {document_id}"

    except Exception as e:
        # Handle failures gracefully and log the error state
        if 'doc' in locals():
            doc.status = 'failed'
            doc.save()
        return f"Error processing document {document_id}: {str(e)}"
from celery import shared_task
from .rag_service import RAGService

@shared_task
def process_document_task(document_id: int, text: str):
    rag = RAGService()
    rag.process_and_store_document(document_id, text)
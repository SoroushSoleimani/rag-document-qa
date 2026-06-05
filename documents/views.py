from rest_framework import viewsets
from .models import Document, QAHistory
from .serializers import DocumentSerializer, QAHistorySerializer
from .tasks import process_document_task

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        document = serializer.save()
        process_document_task.delay(document.id, document.full_text)

class QAHistoryViewSet(viewsets.ModelViewSet):
    queryset = QAHistory.objects.all().order_by('-created_at')
    serializer_class = QAHistorySerializer
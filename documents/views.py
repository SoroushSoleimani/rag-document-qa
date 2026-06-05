from rest_framework import viewsets
from .models import Document, QAHistory
from .serializers import DocumentSerializer, QAHistorySerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer

class QAHistoryViewSet(viewsets.ModelViewSet):
    queryset = QAHistory.objects.all().order_by('-created_at')
    serializer_class = QAHistorySerializer
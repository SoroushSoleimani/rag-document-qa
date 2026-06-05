from rest_framework import serializers
from .models import Document, QAHistory

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'full_text', 'uploaded_at', 'updated_at']
        read_only_fields = ['full_text', 'uploaded_at', 'updated_at']

class QAHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QAHistory
        fields = ['id', 'question', 'answer', 'created_at']
        read_only_fields = ['answer', 'created_at']
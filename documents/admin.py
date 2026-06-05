from django.contrib import admin
from .models import Document, QAHistory

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'updated_at')
    search_fields = ('title', 'full_text')
    # Make the full_text field read-only as it is populated by the system
    readonly_fields = ('full_text', 'uploaded_at', 'updated_at')

@admin.register(QAHistory)
class QAHistoryAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')
    readonly_fields = ('question', 'answer', 'created_at')
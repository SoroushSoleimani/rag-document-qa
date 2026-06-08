from django.contrib import admin
from .models import Document, QAHistory

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'updated_at')
    search_fields = ('title', 'full_text')
    # Make the full_text field read-only as it is populated by the system
    readonly_fields = ('full_text', 'uploaded_at', 'updated_at')
    list_display = ('title', 'uploaded_at', 'status')
    
    # Make status read-only so users can't manually change it
    readonly_fields = ('status',)

@admin.register(QAHistory)
class QAHistoryAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')
    # Removed 'question' from readonly_fields so admin can type the question
    readonly_fields = ('answer', 'created_at')
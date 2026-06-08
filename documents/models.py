from django.db import models
from .utils import extract_text_from_docx
import os
from django.db import models

class Document(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    title = models.CharField(max_length=255, verbose_name="Document Title")
    # Support for docx files
    file = models.FileField(upload_to='docs/', verbose_name="Document File")
    # Store the full text of each document
    full_text = models.TextField(blank=True, null=True, verbose_name="Extracted Text")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Upload Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Date")
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Processing Status"
    )

    def save(self, *args, **kwargs):
        # Save the instance first so the file is stored
        super().save(*args, **kwargs)
        
        # If the file is a docx and no text has been extracted yet
        if self.file and self.file.name.endswith('.docx') and not self.full_text:
            
            self.__class__.objects.filter(pk=self.pk).update(status='processing')
            
            extracted_text = extract_text_from_docx(self.file.path)
            
            if extracted_text:
                self.full_text = extracted_text
                # Update the database safely without Pylance warning
                self.__class__.objects.filter(pk=self.pk).update(full_text=self.full_text)
                
                # --- RAG INTEGRATION: Send text to Vector DB ---
                try:
                    from .rag_service import RAGService
                    rag = RAGService()
                    rag.process_and_store_document(self.pk, self.full_text)
                    
                    self.__class__.objects.filter(pk=self.pk).update(status='completed')
                except Exception as e:
                    print(f"Failed to process RAG pipeline for document {self.pk}: {e}")
                    
                    self.__class__.objects.filter(pk=self.pk).update(status='failed')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

class QAHistory(models.Model):
    question = models.TextField(verbose_name="User Question")
    # Make answer blank/null so the admin doesn't force us to type it
    answer = models.TextField(blank=True, null=True, verbose_name="System Answer")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Asked")

    def save(self, *args, **kwargs):
        # If this is a new question and doesn't have an answer yet
        if not self.pk and not self.answer:
            try:
                from .rag_service import RAGService
                rag = RAGService()
                # Generate the answer using our AI service
                self.answer = rag.ask_question(self.question)
            except Exception as e:
                self.answer = f"Error generating answer: {e}"
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Question: {self.question[:50]}..."

    class Meta:
        verbose_name = "QA History"
        verbose_name_plural = "QA Histories"
from django.db import models
from .utils import extract_text_from_docx
import os

class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name="Document Title")
    # Support for docx files
    file = models.FileField(upload_to='docs/', verbose_name="Document File")
    # Store the full text of each document[cite: 1]
    full_text = models.TextField(blank=True, null=True, verbose_name="Extracted Text")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Upload Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    def save(self, *args, **kwargs):
        # Save the instance first so the file is stored and its path is available
        super().save(*args, **kwargs)
        
        # If the file is a docx and no text has been extracted yet
        if self.file and self.file.name.endswith('.docx') and not self.full_text:
            extracted_text = extract_text_from_docx(self.file.path)
            if extracted_text:
                self.full_text = extracted_text
                # Update the database without calling save() again to avoid recursion
                Document.objects.filter(pk=self.pk).update(full_text=self.full_text)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

# Store the history of questions and answers[cite: 1]
class QAHistory(models.Model):
    question = models.TextField(verbose_name="User Question")
    answer = models.TextField(verbose_name="System Answer")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Asked")

    def __str__(self):
        return f"Question: {self.question[:50]}..."

    class Meta:
        verbose_name = "QA History"
        verbose_name_plural = "QA Histories"
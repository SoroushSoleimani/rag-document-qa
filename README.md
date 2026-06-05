# Intelligent Document RAG System

This project provides a robust REST API for an intelligent document Q&A system. It utilizes Django for the backend, ChromaDB for vector storage, and an LLM (via OpenRouter) to provide accurate answers based on uploaded documents.

## Key Features
- **Automated RAG Pipeline:** Automatically vectorizes uploaded .docx files.
- **AI-Powered Q&A:** Answers user queries by retrieving relevant context from documents.
- **RESTful API:** Full API support via Django REST Framework for integration with external applications.

## API Endpoints
- `/api/documents/` : Upload and manage documents.
- `/api/qa/` : Ask questions and receive AI-generated answers based on uploaded files.

## Tech Stack
- **Backend:** Django & Django REST Framework
- **Vector DB:** ChromaDB
- **LLM Engine:** LangChain & OpenRouter (Llama models)
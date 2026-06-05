# Intelligent RAG Document Question Answering System

## Project Overview
This project is an advanced, asynchronous Question-Answering system built upon the Retrieval-Augmented Generation (RAG) architecture. It is designed to allow users to upload text-heavy documents and naturally query their contents using state-of-the-art Large Language Models (LLMs). By combining a robust web framework with distributed task queues and vector databases, the system ensures high scalability, accurate information retrieval, and an entirely non-blocking user experience.

## Core Architecture and Data Flow
The architecture of this system is strictly divided into three main operational phases: Data Ingestion, Vectorization, and Retrieval-Generation.

1. Document Ingestion Phase:
Users interact with the system through the Django administrative interface. Upon uploading a document, the web server immediately saves the file and registers the metadata in a SQLite database. Instead of blocking the main thread, the server dispatches a background task to a task queue, ensuring the web interface remains highly responsive.

2. Asynchronous Processing and Vectorization Phase:
A dedicated worker process continuously listens to the message broker. Once a new document task is received, the worker extracts the raw text from the document. The text is then passed through a recursive character text splitter to divide the content into meaningful, overlapping chunks. These chunks are transformed into dense vector representations using multilingual sentence-transformer embeddings and persistently stored in an offline vector database.

3. Retrieval-Augmented Generation (RAG) Phase:
When a user submits a query, the system converts the question into a vector using the same embedding model. It then performs a similarity search within the vector database to retrieve the most contextually relevant document chunks. Finally, these chunks, alongside the user's original question, are structured into a strict prompt and sent to an external Large Language Model via an API. The model synthesizes the context and returns a highly accurate, hallucination-free response.

## Technology Stack
The system is built using modern, industry-standard technologies ensuring modularity and performance:

* Web Framework: Django and Django REST Framework are utilized for robust backend management and API endpoints.
* Task Queue and Message Broker: Celery is implemented for background task execution, backed by Redis as the message broker.
* AI and Natural Language Processing: LangChain serves as the orchestration framework for LLM interactions, combined with HuggingFace offline embeddings for data privacy.
* Vector Storage: ChromaDB is integrated as the local vector store for fast similarity search operations.
* External LLM Provider: The system utilizes the OpenRouter API to securely communicate with external language models without the need for heavy local GPU processing.
* Containerization: The entire ecosystem is fully containerized using Docker and Docker Compose, ensuring identical execution environments across development and production.

## System Requirements and Setup Configuration
To deploy and test this system, the host machine must have Docker and Docker Compose installed. Furthermore, an active API key from OpenRouter is required to facilitate communication with the language model.

To configure the environment, you must create a standard environment variables file (named .env) in the root directory of the project. Inside this file, you need to define your API key under the variable name OPENROUTER_API_KEY. 

## Deployment and Execution Guide
Deploying the system is entirely automated through containerization. You simply need to navigate to the project directory using your terminal and instruct Docker Compose to build and bring up the services. The container orchestration will automatically download the necessary Python images, install all dependencies listed in the requirements file, and simultaneously start the Django web server, the Redis broker, and the Celery worker process in isolated environments.

## User Instructions
Once the system is running, the application can be accessed via the local host on port 8000. 

To process a document, navigate to the administrative panel and access the Documents section. Upload your supported document format and save it. You can monitor the background worker terminal to observe the text splitting and vectorization process.

To interact with the processed document, navigate to the QA Histories section in the administrative panel. Enter your question and save the record. The system will independently search the vector database, consult the language model, and update the record with the generated answer based purely on your document's context.

## Author
Soroush Soleimani
Computer Engineering Student, K. N. Toosi University of Technology
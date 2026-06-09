# Enterprise Retrieval-Augmented Generation (RAG) Document QA System

This repository implements a production-ready, distributed Retrieval-Augmented Generation (RAG) system built on top of Django, Celery, Redis, and ChromaDB. The architecture is designed to handle document ingestion, asynchronous text vectorization, and contextual question-answering using advanced large language models via the OpenRouter API.

---

## Architectural Overview

The system transitions away from synchronous monolithic processing by separating the web application runtime from heavy computational operations (document parsing and embedding generation).

### Data Ingestion and Asynchronous Vectorization Flow

1. **Document Ingest:** A user uploads a `.docx` file through the administrative orchestrator (Django). The database immediately commits the record with a `pending` state.
2. **Task Brokerage:** Django dispatches a background task payload to the Redis Message Broker.
3. **Background Worker Execution:** A Celery Worker consumes the task, transitions the document state to `processing`, and invokes the extraction pipeline.
4. **Text Chunking:** The raw text is extracted and partitioned using the `RecursiveCharacterTextSplitter` algorithm with optimal chunk sizing and overlapping to preserve semantic boundaries.
5. **Vector Ingestion:** Document chunks are embedded into high-dimensional vector spaces and persisted into ChromaDB.
6. **State Resolution:** Upon successful serialization and storage, the document state is updated to `completed`.

### Contextual Query Pipeline

When a query is dispatched to the RAG layer:

- The system converts the semantic meaning of the question into a query vector.
- A similarity search is performed across ChromaDB to isolate the top *k* mathematically closest context chunks based on **Cosine Similarity**:

        Similarity = cos(θ) = (A · B) / (||A|| ||B||)

- The isolated contexts are dynamically injected into a deterministic prompt structure.
- The payload is transferred to the `openai/gpt-oss-120b:free` model on OpenRouter, which enforces strict context-bounding to eradicate hallucinations.

## Core Technical Features

- **Asynchronous Task Queuing:** Decouples document tokenization and vector database synchronization from the HTTP request-response cycle using Celery and Redis.
- **Deterministic Status Tracking:** Implements explicit finite state tracking (`pending`, `processing`, `completed`) for granular lifecycle visibility.
- **Source Tracking & Citations:** Every generated response is programmatically appended with detailed source citations, highlighting the exact context snippets pulled from the vector store.
- **Graceful Exception Fallbacks:** Robust error handling layers intercept common infrastructure failures (API authentication faults, rate limits, or network timeouts), providing user-friendly system logs instead of unhandled runtime crashes.
- **Automated Unit Testing:** Includes automated testing coverage targeting model initialization, default states, and string representation accuracy under isolated test databases.

---

## System Tech Stack

- **Web Framework:** Django 5.x
- **API Framework:** Django REST Framework (DRF)
- **Task Queue & Broker:** Celery 5.x / Redis
- **Vector Store & LLM Orchestration:** ChromaDB / LangChain
- **Target Inference Model:** OpenAI GPT-OSS-120B via OpenRouter
- **Containerization:** Docker / Docker Compose

---

## Project Structure

```text
rag-document-qa/
│
├── core/
│   ├── __init__.py          # Bootstraps Celery app configuration
│   ├── celery.py            # Celery instance definitions
│   ├── settings.py          # Global Django settings
│   └── urls.py              # Main routing matrix
│
├── documents/
│   ├── admin.py             # Custom Django Admin interfaces with readonly states
│   ├── models.py            # Database schemas (Document, QAHistory)
│   ├── tasks.py             # Asynchronous Celery task declarations
│   ├── rag_service.py       # Main LangChain, ChromaDB, and OpenRouter integration
│   ├── serializers.py       # DRF serialization configurations
│   ├── tests.py             # Automated unit test suites
│   └── views.py             # ViewSets for endpoints layout
│
├── docker-compose.yml       # Multi-container orchestration specification
├── Dockerfile               # Web/Worker container environment blueprint
└── requirements.txt         # Deterministic python dependency manifest
```


---



## Installation & Local Deployment

### Prerequisites

- Docker Engine installed locally
- Docker Compose V2 plugin active

### 1. Environment Configuration

Create a `.env` file in the root directory of the project alongside the `docker-compose.yml` file and define your OpenRouter credential token:

```env
OPENROUTER_API_KEY=your_actual_openrouter_api_key_here
```

2. Multi-Container Execution
Launch the entire localized ecosystem (Web runtime, Celery background worker, and Redis server) using Docker Compose:

```bash
docker compose up --build
```

This command automatically resolves dependencies, configures internal networking, maps database migrations, and exposes the application gateway.

3. Application Accessibility
Django Administrative Panel: http://127.0.0.1:8000/admin/

Browsable REST API Interface: http://127.0.0.1:8000/api/




---



## Automated Quality Assurance (Testing)

The system enforces software stability metrics via automated test structures. To execute the internal unit tests within the isolated Docker application boundary without impacting production storage:

```bash
docker compose exec web python manage.py test documents
```

```text
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
```
```text
----------------------------------------------------------------------
Ran 2 tests in 0.004s
```

OK
Destroying test database for alias 'default'...



## API Endpoints Documentation

The system exposes programmatic gateways for integration with external frontend applications or analytical toolsets:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/documents/` | `GET` | Lists all uploaded documents, metadata, and extraction states. |
| `/api/documents/` | `POST` | Ingests a new `.docx` file and triggers the async vectorization pipeline. |
| `/api/documents/<id>/` | `GET` | Retrieves explicit data instance records for a specified file ID. |
| `/api/qa/` | `POST` | Accepts user queries, runs similarity retrieval, and extracts bounded model responses. |

---


```text
## Additional Notes

- **File Support:** The system currently supports only `.docx` files for ingestion. Extending to other formats (PDF, TXT) requires modifying the extraction pipeline in `rag_service.py`.
- **Rate Limits:** The OpenRouter free tier model (`openai/gpt-oss-120b:free`) has rate limits. For production use, consider upgrading to a paid model and adjusting the RAG service configuration.
- **Vector Persistence:** ChromaDB persists vectors locally by default. For distributed deployments, use a persistent Docker volume or switch to a cloud-native vector database (e.g., Pinecone, Weaviate).
- **Task Monitoring:** All asynchronous tasks are monitored via Celery logs. To inspect task status, integrate `django-celery-results` or check the `QAHistory` table in the database.
- **Error Handling:** The system includes graceful fallbacks for API authentication faults, network timeouts, and rate limits – errors are logged without crashing the worker.
```

## License

This project is provided as-is for educational and production reference. Modify and distribute according to your organization's policies.
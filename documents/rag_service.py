import os
import dotenv
from django.conf import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI

# Load variables from .env file
dotenv.load_dotenv()

class RAGService:
    def __init__(self):
        # 1. Initialize offline Embeddings for Vector DB
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        self.persist_directory = os.path.join(settings.BASE_DIR, 'chroma_db')
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory, 
            embedding_function=self.embeddings
        )
        
        # 2. Initialize the LLM using OpenRouter API (FREE TIER)
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
             raise ValueError("OPENROUTER_API_KEY is missing from .env file.")

        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            model_name="openrouter/free",
            max_tokens=512,
            temperature=0.3 
        )

    def process_and_store_document(self, document_id: int, text: str):
        """Splits the text and stores it in ChromaDB."""
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = text_splitter.split_text(text)
            metadatas = [{"document_id": document_id} for _ in chunks]
            self.vectorstore.add_texts(texts=chunks, metadatas=metadatas)
            print(f"Successfully vectorized document ID: {document_id}")
        except Exception as e:
            print(f"Error vectorizing document {document_id}: {e}")

    def ask_question(self, question: str) -> str:
        """Finds relevant chunks and asks the LLM manually."""
        try:
            docs = self.vectorstore.similarity_search(question, k=3)
            
            context = "\n\n".join([doc.page_content for doc in docs])

            prompt = f"""You are an intelligent assistant. Use the following pieces of retrieved context to answer the question accurately. If you don't know the answer based on the context, say that you don't know.

Context:
{context}

Question:
{question}

Answer:"""

            response = self.llm.invoke(prompt)
            
            return response.content
            
        except Exception as e:
            print(f"LLM Generation Error: {e}")
            return f"An error occurred: {e}"
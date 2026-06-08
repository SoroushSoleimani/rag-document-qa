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
            base_url="https://openrouter.ai/api/v1",
            model_name="openai/gpt-oss-120b:free",
            max_tokens=512,
            temperature=0.3 
        )

    def process_and_store_document(self, document_id: int, text: str):
        """Splits the text and stores it in ChromaDB."""
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = text_splitter.split_text(text)
            
            metadatas = [{"document_id": str(document_id)} for _ in chunks]
            
            self.vectorstore.add_texts(texts=chunks, metadatas=metadatas)
            print(f"Successfully vectorized document ID: {document_id}")
        except Exception as e:
            print(f"Error vectorizing document {document_id}: {e}")

    import os


    def ask_question(self, question: str) -> str:
        """
        Finds relevant chunks, asks the LLM, and appends the source citations.
        Includes graceful error handling for missing API keys or network issues.
        """
        # 0. Fast-fail validation: Check for API key before processing
        if not os.getenv("OPENROUTER_API_KEY"):
            return " **Configuration Error:** OpenRouter API key is missing. Please check your environment variables."

        try:
            # 1. Retrieve relevant context from ChromaDB
            docs = self.vectorstore.similarity_search(question, k=3)
            
            # If no documents are found, return a polite warning
            if not docs:
                return " **Not Found:** No relevant context could be found in the uploaded documents to answer your question. Please ensure a document is successfully processed first."

            context = "\n\n".join([doc.page_content for doc in docs])

            # 2. Extract source metadata for citations programmatically
            citations = []
            for i, doc in enumerate(docs):
                snippet = doc.page_content[:60].replace('\n', ' ') + "..."
                citations.append(f"[{i+1}] Context Snippet: '{snippet}'")
            
            citations_text = "\n".join(citations)

            # 3. Prepare the prompt structure for the LLM
            # 3. Prepare the prompt structure for the LLM
            prompt = f"""You are an expert analyst. Answer the question based ONLY on the provided context. 
Please provide a complete, well-structured sentence. If there is additional relevant explanation in the context, include it briefly.
If the answer is not in the context, say 'I don't know'.

Context:
{context}

Question:
{question}

Answer:"""

            # 4. Invoke the LLM
            response = self.llm.invoke(prompt)
            answer = response.content
            
            # 5. Combine the AI's answer with the exact extracted sources
            final_output = f"{answer}\n\n---\n** Source Tracking:**\n{citations_text}"
            
            return final_output

        except Exception as e:
            error_msg = str(e)
            print(f"LLM Generation Error: {error_msg}")
            
            # Provide user-friendly error messages based on common API exceptions
            if "authentication" in error_msg.lower() or "401" in error_msg:
                return " **Authentication Error:** Failed to authenticate with the AI provider. Your API key might be invalid or expired."
            elif "rate limit" in error_msg.lower() or "429" in error_msg:
                return " **Rate Limit Exceeded:** The AI provider is currently busy. Please wait a moment and try saving again."
            else:
                return f" **System Error:** An unexpected error occurred while communicating with the AI model.\n\n*Technical Details: {error_msg}*"
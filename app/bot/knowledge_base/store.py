from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from app.config import settings
from app.admin.knowledge_base.store import list_documents
from app.bot.knowledge_base.preprocess import KnowledgeBasePreprocessor
import chromadb

class KnowledgeBaseStore(ABC):
    """Abstract base class defining the knowledge base interface."""
    
    @abstractmethod
    async def index(self) -> None:
        """Index all documents from knowledge base."""
        pass
    
    @abstractmethod
    async def query(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Query the knowledge base using a vector and return matching documents."""
        pass

class ChromaKnowledgeBaseStore(KnowledgeBaseStore):
    """ChromaDB implementation of the knowledge base interface."""
    
    def __init__(self):
        # Initialize Spacy embeddings
        self.embeddings = SpacyEmbeddings()
        
        # Configure Chroma client
        self.client = Chroma(
            collection_name="knowledge_base",
            embedding_function=self.embeddings,
            persist_directory=settings.get("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        )
    
    async def index(self, docs) -> None:
        """Index all documents from knowledge base into ChromaDB."""
        # Get all documents from knowledge base
        # Add documents to Chroma
        self.client.add_documents(docs)
        self.client.persist()
    
    async def query(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Query ChromaDB using a vector and return matching documents.
        
        Args:
            query: The query to search with
            top_k: Number of results to return (default: 5)
            
        Returns:
            List of matching documents with their similarity scores
        """

        query_vector = self.embeddings.embed_query(query)

        results = vector_store.similarity_search_by_vector(
            embedding=query_vector, k=1
        )
        
        # Format results
        matches = []
        for doc, score in results:
            matches.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)
            })
        
        return matches
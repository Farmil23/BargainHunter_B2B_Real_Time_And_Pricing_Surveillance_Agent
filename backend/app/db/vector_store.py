from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from backend.app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class PineconeStore:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.dimension = settings.PINECONE_DIMENSION
        
        # Ensure index exists
        self._ensure_index()
        
        self.index = self.pc.Index(self.index_name)
        # We use standard OpenAI text-embedding-3-small or text-embedding-ada-002 (which usually has diff dimension, but let's assume dim=1024 is configured for a specific model or we pad/truncate)
        # E.g. text-embedding-3-large can be set to 1024 dimensions.
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", 
            dimensions=self.dimension,
            openai_api_key=settings.OPENAI_API_KEY
        )

    def _ensure_index(self):
        if self.index_name not in self.pc.list_indexes().names():
            logger.info(f"Creating Pinecone index: {self.index_name} with dim {self.dimension}")
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

    def upsert_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        """Upsert text documents with embeddings to Pinecone."""
        vectors = []
        for i, doc in enumerate(documents):
            embed = self.embeddings.embed_query(doc)
            vectors.append({
                "id": ids[i],
                "values": embed,
                "metadata": metadatas[i]
            })
        
        self.index.upsert(vectors=vectors)
        
    def similarity_search(self, query: str, top_k: int = 3):
        """Search Pinecone for similar documents."""
        query_embedding = self.embeddings.embed_query(query)
        result = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        return result

# Singleton instance
vector_store = PineconeStore()

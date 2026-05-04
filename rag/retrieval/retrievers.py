from typing import List

from db.base_vector import BaseVectorStore
from db.dto import Chunk
from rag.embeddings.base import BaseEmbedder
from rag.retrieval.base import BaseRetriever


class SimpleRetriever(BaseRetriever):
    
    def __init__(self, embedder: BaseEmbedder, store: BaseVectorStore, top_k: int = 5):
        self.embedder = embedder
        self.store = store
        self.top_k = top_k
    
    def retrieve(self, query: str) -> List[Chunk]:
        query_vec = self.embedder.embed(query)
        return self.store.search(query_vec, limit=self.top_k)
    
    def batch_retrieve(self, queries: List[str]) -> List[List[Chunk]]:
        return [self.retrieve(q) for q in queries]
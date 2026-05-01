from embeddings.base import BaseEmbedder
from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbedder(BaseEmbedder):

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        
        embedding = self.model.encode(text, normalize_embeddings=True)
        
        return embedding.tolist()
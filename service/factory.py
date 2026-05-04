from config.schema import ChunkingConfig, EmbeddingConfig, LLMConfig, RetrievalConfig
from db.base_vector import BaseVectorStore
from rag.chunking.chunkers import SlidingWindowChunker
from rag.embeddings.base import BaseEmbedder
from rag.embeddings.sentence_transformer import SentenceTransformerEmbedder
from rag.llm.gemini_llm import GeminiLLM
from rag.retrieval.retrievers import SimpleRetriever


def create_embedder(config: EmbeddingConfig):
    if config.provider == "sentence_transformer":
        return SentenceTransformerEmbedder(config.model)
    raise ValueError("Unknown embedder")

def create_llm(config: LLMConfig):
    if config.provider == "gemini":
        return GeminiLLM(api_key=config.api_key, model=config.model)
    raise ValueError("Unknown LLM")

def create_chunker(config: ChunkingConfig):
    if config.model == "sliding_window":
        return SlidingWindowChunker(size=config.size, overlap=config.overlap)
    raise ValueError("Unknown chunker")

def create_retriever(embedder: BaseEmbedder, store: BaseVectorStore, config: RetrievalConfig):
    if config.model == "simple":
        return SimpleRetriever(embedder=embedder, store=store, top_k=config.top_k)
    raise ValueError("Unknown retriever")
import hashlib
from typing import List

from fastapi import UploadFile

from config.schema import AppConfig
from db.dto import Chunk
from db.qdrant import QdrantStore
from rag.prompting.prompt_builder import PromptBuilder
from service.factory import create_chunker, create_embedder, create_llm, create_retriever
from utils.pdf_reader import PDFReader


def make_doc_id(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class RAGService:
    
    def __init__(self, config: AppConfig):
        self.config = config

        self.store = QdrantStore(
            url=config.vector_db.url,
            collection_name=f"{config.domain}_{config.embedding.model}",
            vector_size=config.embedding.size
        )

        self.pdf_reader = PDFReader()

        self.embedder = create_embedder(config.embedding)
        self.llm = create_llm(config.llm)
        self.chunker = create_chunker(config.chunking)
        self.retriever = create_retriever(self.embedder, self.store, config.retrieval)

        prompt_cfg = config.llm_prompt
        custom = prompt_cfg.custom_template

        self.prompt_builder = PromptBuilder(
            use_custom=prompt_cfg.use_custom,
            template_name=prompt_cfg.template_name,
            system_prompt=custom.system_prompt,
            context_intro=custom.context_intro,
            question_prefix=custom.question_prefix,
            answer_instruction=custom.answer_instruction,
            include_title=custom.include_title,
            include_score=custom.include_score,
            score_precision=custom.score_precision
        )

    def ingest(self, file: UploadFile) -> str:
        
        text = self.pdf_reader.read(file)
        if not text.strip():
            return "Не удалось извлечь текст из PDF"
        
        doc_id = make_doc_id(text)
        if self.store.get_by_doc_id(doc_id):
            return "Документ уже существует"

        chunks_text = self.chunker.chunk(text)
        chunks: List[Chunk] = [
            Chunk(text=chunk_text, doc_id=doc_id, chunk_id=i)
            for i, chunk_text in enumerate(chunks_text)
        ]
        vectors = [self.embedder.embed(chunk.text) for chunk in chunks]
        self.store.add(vectors, chunks)

        return f"Индексировано {len(chunks)} chunks"

    def query(self, question: str) -> str:
        chunks = self.retriever.retrieve(question)
        prompt = self.prompt_builder.build(question, chunks)
        answer = self.llm.generate(prompt)

        return answer
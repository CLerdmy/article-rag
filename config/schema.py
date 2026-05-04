from dataclasses import dataclass


@dataclass
class VectorDBConfig:
    url: str

@dataclass
class EmbeddingConfig:
    type: str
    provider: str
    model: str
    size: int

@dataclass
class LLMConfig:
    type: str
    provider: str
    model: str
    api_key: str

@dataclass
class ChunkingConfig:
    model: str
    size: int
    overlap: int

@dataclass
class RetrievalConfig:
    model: str
    top_k: int

@dataclass
class PromptCustomConfig:
    include_title: bool
    include_score: bool
    score_precision: int
    system_prompt: str
    context_intro: str
    question_prefix: str
    answer_instruction: str

@dataclass
class PromptConfig:
    use_custom: bool
    template_name: str
    custom_template: PromptCustomConfig

@dataclass
class AppConfig:
    domain: str
    vector_db: VectorDBConfig
    embedding: EmbeddingConfig
    llm: LLMConfig
    chunking: ChunkingConfig
    retrieval: RetrievalConfig
    llm_prompt: PromptConfig
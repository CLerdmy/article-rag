import json
from pathlib import Path
from typing import Optional

from config.schema import (
    AppConfig,
    ChunkingConfig,
    EmbeddingConfig,
    LLMConfig,
    PromptConfig,
    PromptCustomConfig,
    RetrievalConfig,
    VectorDBConfig,
)


CONFIG_PATH = Path(__file__).parent / "config.json"
_CONFIG_CACHE: Optional[AppConfig] = None


def load_config() -> AppConfig:
    global _CONFIG_CACHE

    if _CONFIG_CACHE is None:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)

        _CONFIG_CACHE = AppConfig(
            domain=raw["domain"],
            vector_db=VectorDBConfig(**raw["vector_db"]),
            embedding=EmbeddingConfig(**raw["embedding"]),
            llm=LLMConfig(**raw["llm"]),
            chunking=ChunkingConfig(**raw["chunking"]),
            retrieval=RetrievalConfig(**raw["retrieval"]),
            llm_prompt=PromptConfig(
                use_custom=raw["llm_prompt"]["use_custom"],
                template_name=raw["llm_prompt"]["template_name"],
                custom_template=PromptCustomConfig(**raw["llm_prompt"]["custom_template"])
            )
        )

    return _CONFIG_CACHE
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    doc_id: str
    chunk_id: int
    score: float | None = None

    def to_payload(self) -> dict:
        return {
            "text": self.text,
            "doc_id": self.doc_id,
            "chunk_id": self.chunk_id
        }

    @classmethod
    def from_payload(cls, payload: dict, score: float | None = None):
        return cls(
            text=payload["text"],
            doc_id=payload["doc_id"],
            chunk_id=payload["chunk_id"],
            score=score
        )
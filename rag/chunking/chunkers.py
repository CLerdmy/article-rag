from rag.chunking.base import BaseChunker


class SlidingWindowChunker(BaseChunker):
    def __init__(self, size: int, overlap: int):
        self.size = size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.size
            chunks.append(text[start:end])
            start += self.size - self.overlap

        return chunks
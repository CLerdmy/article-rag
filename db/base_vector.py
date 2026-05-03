from abc import ABC, abstractmethod
from typing import List

from db.dto import Chunk


class BaseVectorStore(ABC):

    @abstractmethod
    def add(self, vectors: List[List[float]], chunks: List[Chunk]) -> None:
        pass

    @abstractmethod
    def search(self, query_vector: List[float], limit: int) -> List[Chunk]:
        pass

    @abstractmethod
    def delete_by_doc_id(self, doc_id: str) -> None:
        pass

    @abstractmethod
    def get_by_doc_id(self, doc_id: str) -> List[Chunk]:
        pass
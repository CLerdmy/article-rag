from abc import ABC, abstractmethod
from typing import List

from db.dto import Chunk


class BaseRetriever(ABC):
    
    @abstractmethod
    def retrieve(self, query: str) -> List[Chunk]:
        pass
    
    @abstractmethod
    def batch_retrieve(self, queries: List[str]) -> List[List[Chunk]]:
        pass
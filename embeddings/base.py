from abc import ABC, abstractmethod


class BaseEmbedder(ABC):

    @abstractmethod
    def emb(self, text: str):
        pass
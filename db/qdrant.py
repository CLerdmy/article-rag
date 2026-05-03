import uuid
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from db.base_vector import BaseVectorStore
from db.dto import Chunk


class QdrantStore(BaseVectorStore):

    def __init__(self, url: str, collection_name: str, vector_size: int):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size

        self._ensure_collection()

    def _ensure_collection(self):
        if self.collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )

    def add(self, vectors: List[List[float]], chunks: List[Chunk]) -> None:
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=chunk.to_payload()
            )
            for vector, chunk in zip(vectors, chunks)
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_vector: list[float], limit: int = 5) -> list[Chunk]:
        result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True
        )

        return [
            Chunk.from_payload(point.payload, score=point.score)
            for point in result.points
        ]

    def delete_by_doc_id(self, doc_id: str) -> None:
        self.client.delete(
            collection_name=self.collection_name,
            points_selector={
                "filter": {
                    "must": [
                        {"key": "doc_id", "match": {"value": doc_id}}
                    ]
                }
            }
        )

    def get_by_doc_id(self, doc_id: str) -> list[Chunk]:
        points, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {"key": "doc_id", "match": {"value": doc_id}}
                ]
            },
            with_payload=True
        )

        return [
            Chunk.from_payload(point.payload)
            for point in points
        ]
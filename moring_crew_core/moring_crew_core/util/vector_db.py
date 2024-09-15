import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import os
from config.settings import CACHE_DIR

class VectorDB:
    def __init__(self, collection_name: str = "PostDocCollection"):
        persist_directory = os.path.join(CACHE_DIR, "chroma_db")
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self._get_or_create_collection(collection_name)

    def _get_or_create_collection(self, collection_name: str):
        try:
            return self.client.get_collection(name=collection_name)
        except ValueError:
            return self.client.create_collection(name=collection_name)

    def add_documents(self, documents: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]] = None, ids: List[str] = None):
        if ids is None:
            ids = [str(i) for i in range(len(documents))]
        if metadatas is None:
            metadatas = [{} for _ in documents]
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query_embedding: List[float], n_results: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return [
            {
                "id": id,
                "document": document,
                "metadata": metadata,
                "distance": distance
            }
            for id, document, metadata, distance in zip(
                results['ids'][0],
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )
        ]

    def get_document(self, id: str) -> Dict[str, Any]:
        result = self.collection.get(ids=[id])
        return {
            "id": result['ids'][0],
            "document": result['documents'][0],
            "metadata": result['metadatas'][0]
        }

    def update_document(self, id: str, document: str, embedding: List[float], metadata: Dict[str, Any] = None):
        self.collection.update(
            ids=[id],
            documents=[document],
            embeddings=[embedding],
            metadatas=[metadata] if metadata else None
        )

    def delete_document(self, id: str):
        self.collection.delete(ids=[id])

    def list_collections(self) -> List[str]:
        return [collection.name for collection in self.client.list_collections()]

    def delete_collection(self, collection_name: str):
        self.client.delete_collection(name=collection_name)

    def get_collection_stats(self) -> Dict[str, Any]:
        return {
            "count": self.collection.count(),
            "name": self.collection.name
        }
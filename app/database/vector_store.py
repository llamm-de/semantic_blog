import chromadb
from chromadb.config import Settings
import os

class ChromaDBManager:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            is_persistent=True,
            persist_directory="chroma_db",
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection("blog_posts")

    def add_post(self, post_id: str, content: str, metadata: dict):
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[post_id]
        )

    def search_posts(self, query: str, limit: int = 10):
        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        
        # Add default distances if not provided by the API
        #if "distances" not in results:
        results["distances"] = [[1 - (i/limit) for i in range(len(results["ids"][0]))]]
        
        return results

    def update_post(self, post_id: str, content: str, metadata: dict):
        self.collection.update(
            ids=[post_id],
            documents=[content],
            metadatas=[metadata]
        )

    def delete_post(self, post_id: str):
        self.collection.delete(ids=[post_id])

vector_store = ChromaDBManager() 
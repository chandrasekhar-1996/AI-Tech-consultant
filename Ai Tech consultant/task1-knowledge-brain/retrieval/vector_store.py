import os
import uuid
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

class RetrievalEngine:
    def __init__(self, collection_name: str = "knowledge_brain"):
        # Uses temporary persistence layer or standard paths
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY", "mock-key"),
            model_name="text-embedding-3-small"
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.openai_ef
        )

    def chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            if i + chunk_size >= len(words):
                break
        return chunks

    def add_document(self, url: str, title: str, content: str):
        chunks = self.chunk_text(content)
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [{"url": url, "title": title} for _ in chunks]
        
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )

    def query_knowledge(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        output = []
        if results and results["documents"]:
            for doc, meta, score in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
                output.append({
                    "content": doc,
                    "metadata": meta,
                    "distance": score
                })
        return output

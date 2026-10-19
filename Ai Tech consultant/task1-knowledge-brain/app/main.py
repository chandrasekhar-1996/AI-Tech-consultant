from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any
import os

from task1_knowledge_brain.ingestion.parser import KnowledgeIngestor
from task1_knowledge_brain.retrieval.vector_store import RetrievalEngine

app = FastAPI(title="Task 1: Knowledge Brain API")
ingestor = KnowledgeIngestor()
retrieval = RetrievalEngine()

class IngestRequest(BaseModel):
    url: HttpUrl

class QueryRequest(BaseModel):
    query: str
    n_results: int = 3

class MultimodalRequest(BaseModel):
    image_url: str
    prompt: str

@app.post("/ingest")
async def ingest_url(payload: IngestRequest):
    try:
        data = await ingestor.fetch_and_parse(str(payload.url))
        retrieval.add_document(data["url"], data["title"], data["content"])
        return {"status": "success", "message": f"Successfully ingested {payload.url}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=List[Dict[str, Any]])
async def query_brain(payload: QueryRequest):
    try:
        return retrieval.query_knowledge(payload.query, payload.n_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/multimodal/analyze")
async def analyze_image(payload: MultimodalRequest):
    # Simulated execution route for structured vision model workflows
    return {
        "status": "processed",
        "analysis": f"Simulated Vision metrics extracted for visual components matching prompt: '{payload.prompt}'"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

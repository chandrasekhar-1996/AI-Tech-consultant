import httpx
from typing import List, Dict, Any

class KnowledgeBrainClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def fetch_relevant_context(self, search_query: str) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/query",
                    json={"query": search_query, "n_results": 2},
                    timeout=5.0
                )
                if response.status_code == 200:
                    results = response.json()
                    context_blocks = [r["content"] for r in results]
                    return "\n---\n".join(context_blocks)
            except Exception:
                pass
        return "Fallback: Operational default baseline infrastructure profile."

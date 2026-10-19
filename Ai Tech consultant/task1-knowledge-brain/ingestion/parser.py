import httpx
from bs4 import BeautifulSoup
from typing import Dict, Any

class KnowledgeIngestor:
    def __init__(self):
        self.headers = {"User-Agent": "AI-Tech-Consultant-Brain/1.0"}

    async def fetch_and_parse(self, url: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0, headers=self.headers) as client:
            response = await client.get(url)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Strip script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        title = soup.title.string if soup.title else ""
        text = " ".join(soup.stripped_strings)
        
        return {
            "url": url,
            "title": title.strip() if title else "Untitled",
            "content": text
        }

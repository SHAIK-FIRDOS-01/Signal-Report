import os
import httpx
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class NewsIngestionService:
    """
    Service for fetching news from the GNews API asynchronously.
    Includes rate-limiting and fail-safe logic.
    """
    
    def __init__(self):
        self.api_key = os.getenv('GNEWS_API_KEY')
        self.search_url = "https://gnews.io/api/v4/search"
        self.headlines_url = "https://gnews.io/api/v4/top-headlines"
        self.max_retries = 3

    async def _make_request(self, url: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        import asyncio
        async with httpx.AsyncClient() as client:
            for attempt in range(self.max_retries):
                try:
                    response = await client.get(url, params=params, timeout=20.0)
                    
                    if response.status_code == 429:
                        wait_time = (2 ** attempt) + 1
                        logger.warning(f"Rate limit exceeded. Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                        continue

                    response.raise_for_status()
                    data = response.json()
                    return data.get('articles', [])
                except httpx.HTTPStatusError as e:
                    logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                    if e.response.status_code in [500, 502, 503, 504]:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    break
                except httpx.RequestError as e:
                    logger.error(f"Request error: {str(e)}")
                    await asyncio.sleep(2 ** attempt)
            return []

    async def fetch_news(
        self, 
        query: str = "AI advancements", 
        lang: str = "en", 
        max_results: int = 10,
        from_date: str = None,
        to_date: str = None
    ) -> List[Dict[str, Any]]:
        if not self.api_key or self.api_key == "your_gnews_api_key_here":
            return []
        
        params = {
            'q': query,
            'lang': lang,
            'max': max_results,
            'apikey': self.api_key,
            'sortby': 'publishedAt'
        }
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
            
        return await self._make_request(self.search_url, params)

    async def fetch_top_headlines(
        self, 
        category: str = "technology", 
        lang: str = "en", 
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        if not self.api_key:
            return []
        params = {
            'category': category,
            'lang': lang,
            'max': max_results,
            'apikey': self.api_key
        }
        return await self._make_request(self.headlines_url, params)

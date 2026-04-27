import os
import httpx
import asyncio
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

async def test_gnews_today():
    api_key = os.getenv('GNEWS_API_KEY')
    base_url = "https://gnews.io/api/v4/search"
    
    # Try from today UTC
    today = datetime.now(timezone.utc).strftime('%Y-%m-%dT00:00:00Z')
    print(f"Searching from: {today}")
    
    params = {
        'q': "AI OR technology OR world",
        'lang': "en",
        'max': 10,
        'apikey': api_key,
        'from': today,
        'sortby': 'publishedAt'
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"Fetched {len(articles)} articles.")
            for art in articles:
                print(f"- {art['publishedAt']}: {art['title']}")
        else:
            print(response.text)

if __name__ == "__main__":
    asyncio.run(test_gnews_today())

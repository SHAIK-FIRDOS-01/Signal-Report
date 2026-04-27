import os
import django
import asyncio
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.knowledge_base.tasks import trigger_news_ingestion
from apps.knowledge_base.models import KnowledgeBaseNode

async def test_ingestion():
    print("Initial count:", await sync_to_async(KnowledgeBaseNode.objects.count)())
    
    # Trigger ingestion
    new_ids = await trigger_news_ingestion("AI technology breakthrough")
    print(f"Ingested {len(new_ids)} new articles.")
    
    # Check latest articles
    latest_articles = await sync_to_async(lambda: list(KnowledgeBaseNode.objects.order_by('-published_at')[:5]))()
    print("Latest articles:")
    for art in latest_articles:
        print(f"- {art.published_at}: {art.title}")

if __name__ == "__main__":
    asyncio.run(test_ingestion())

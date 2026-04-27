import asyncio
import logging
from asgiref.sync import sync_to_async
from django.utils import timezone

from .models import KnowledgeBaseNode, EmbeddingStatus
from services.news_ingestion import NewsIngestionService
from services.nlp_processing import NLPProcessingService
from services.ai_service import AIService
from services.scraper_service import ContentScraperService

from django.core.cache import cache
from datetime import timedelta

logger = logging.getLogger(__name__)

INGESTION_LOCK_KEY = "news_ingestion_lock"
INGESTION_LOCK_TIMEOUT = 600  # 10 minutes

async def full_system_ingestion(is_historical: bool = False):
    """
    Enterprise-level orchestration for fetching news across all categories.
    Now includes full-content scraping.
    """
    # 1. Acquire Distributed Lock
    lock_acquired = cache.add(INGESTION_LOCK_KEY, "true", INGESTION_LOCK_TIMEOUT)
    if not lock_acquired:
        logger.warning("Ingestion already in progress. Skipping this run.")
        return False

    try:
        logger.info(f"Starting {'Historical ' if is_historical else 'Latest '}Full System Ingestion...")
        
        categories = {
            "All": "general OR world news",
            "Finance": "finance OR business OR economy OR markets",
            "Tech": "technology OR AI OR software OR gadgets",
            "Politics": "politics OR government OR elections OR policy",
            "Sports": "sports OR athletics",
            "Health": "health OR medicine OR wellness",
            "Science": "science OR space OR research"
        }

        # Calculate dates for historical window (30 days ago)
        from_date = None
        if is_historical:
            thirty_days_ago = timezone.now() - timedelta(days=30)
            from_date = thirty_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

        ingestion_service = NewsIngestionService()
        scraper_service = ContentScraperService()
        total_created = 0

        for label, query in categories.items():
            logger.info(f"Fetching news for category: {label}")
            
            articles = await ingestion_service.fetch_news(
                query=query, 
                from_date=from_date,
                max_results=15 if is_historical else 10
            )
            
            for art in articles:
                # Create Node (minimal data initially)
                node, created = await sync_to_async(KnowledgeBaseNode.objects.get_or_create)(
                    source_url=art['url'],
                    defaults={
                        'title': art['title'],
                        'content_raw': art['content'],
                        'published_at': art.get('publishedAt', timezone.now()),
                        'category': label
                    }
                )
                if created:
                    total_created += 1
                    # Enterprise Logic: Scrape full text immediately
                    full_text = await scraper_service.scrape_full_content(art['url'])
                    if full_text:
                        node.full_text_scraped = full_text
                        await sync_to_async(node.save)(update_fields=['full_text_scraped'])
                    
                    # AI Processing is now deferred to user click (dynamic)

        logger.info(f"Ingestion completed. {total_created} new articles added and scraped.")
        return True

    except Exception as e:
        logger.error(f"Full system ingestion failed: {str(e)}")
        return False
    finally:
        cache.delete(INGESTION_LOCK_KEY)

async def process_article_pipeline(article_id: int):
    """
    Enrichment pipeline that uses full scraped text if available.
    """
    try:
        node = await sync_to_async(KnowledgeBaseNode.objects.get)(id=article_id)
        
        if node.embedding_status == EmbeddingStatus.COMPLETED and node.content_processed:
            logger.info(f"Article {article_id} already processed. Skipping.")
            return

        node.embedding_status = EmbeddingStatus.PROCESSING
        await sync_to_async(node.save)(update_fields=['embedding_status'])

        
        logger.info(f"Starting pipeline for article: {node.title}")

        # Use full text if we have it, otherwise fallback to GNews snippet
        analysis_content = node.full_text_scraped or node.content_raw

        # 2. NLP Processing
        nlp_service = NLPProcessingService()
        nlp_result = await nlp_service.process_content(analysis_content)
        
        # 3. AI Service (Uses full text for deep analysis)
        ai_service = AIService()
        ai_result = await ai_service.enhance_and_vectorize(
            content=analysis_content, 
            nlp_context=nlp_result
        )

        # 4. Update Node
        enhanced_content = ai_result.get('enhanced_content', node.content_raw)
        node.content_processed = enhanced_content
        node.embedding_vector = ai_result.get('vector')
        node.source_credibility_score = ai_result.get('credibility_score', 0.5)
        
        if enhanced_content.startswith("FALLBACK_MODE"):
            node.embedding_status = EmbeddingStatus.FAILED
            node.fail_reason = "AI Processing Fallback: Quota exceeded or API error."
        else:
            node.embedding_status = EmbeddingStatus.COMPLETED
            
        await sync_to_async(node.save)()
        logger.info(f"Successfully processed article: {node.title}")

    except KnowledgeBaseNode.DoesNotExist:
        logger.error(f"Article with id {article_id} not found.")
    except Exception as e:
        logger.error(f"Pipeline failed for article {article_id}: {str(e)}")
        if 'node' in locals():
            node.embedding_status = EmbeddingStatus.FAILED
            node.fail_reason = str(e)
            await sync_to_async(node.save)(update_fields=['embedding_status', 'fail_reason'])


async def trigger_news_ingestion(query: str = "AI advancements"):
    """
    Legacy background task for backward compatibility.
    """
    return await full_system_ingestion(is_historical=False)

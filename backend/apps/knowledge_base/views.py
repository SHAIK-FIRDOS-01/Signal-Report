import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from asgiref.sync import async_to_sync
from django_ratelimit.decorators import ratelimit

from .models import KnowledgeBaseNode
from .tasks import process_article_pipeline, trigger_news_ingestion
from apps.accounts.utils import require_jwt

@method_decorator(require_jwt, name='dispatch')
# @method_decorator(cache_page(60 * 5), name='dispatch') # Cache for 5 mins
@method_decorator(vary_on_headers('Authorization'), name='dispatch')
class DashboardView(View):
    """ Main dashboard API endpoint. """
    def get(self, request):
        from django.utils import timezone
        from datetime import timedelta
        import asyncio
        import threading
        
        latest_node = KnowledgeBaseNode.objects.order_by('-created_at').first()
        is_fresh_install = not latest_node
        needs_ingestion = False
        
        if is_fresh_install:
            needs_ingestion = True
        elif latest_node.created_at < timezone.now() - timedelta(hours=1):
            needs_ingestion = True

        if needs_ingestion:
            from .tasks import full_system_ingestion
            
            # Enterprise Pattern: Trigger background task without blocking the user
            # In a Celery setup, this would be: full_system_ingestion.delay(is_historical=is_fresh_install)
            def run_ingestion():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(full_system_ingestion(is_historical=is_fresh_install))
                loop.close()
            
            thread = threading.Thread(target=run_ingestion)
            thread.daemon = True  # Ensure thread dies when main process dies
            thread.start()

        nodes = KnowledgeBaseNode.objects.all().order_by('-published_at')
        
        # Category filter
        category = request.GET.get('category', 'All')
        if category != 'All':
            nodes = nodes.filter(category__iexact=category)
            
        data = [{
            'id': node.id,
            'title': node.title,
            'category': node.category,
            'content_raw': node.content_raw,
            'full_text_scraped': node.full_text_scraped,
            'content_processed': node.content_processed,
            'embedding_status': node.embedding_status,
            'published_at': node.published_at.isoformat() if node.published_at else None,
            'source_url': node.source_url
        } for node in nodes[:20]]
        return JsonResponse({'nodes': data})

@method_decorator(require_jwt, name='dispatch')
class SearchView(View):
    """ Global search API endpoint. """
    def get(self, request):
        query = request.GET.get('q', '')
        nodes = KnowledgeBaseNode.objects.filter(title__icontains=query) | KnowledgeBaseNode.objects.filter(content_raw__icontains=query)
        data = [{
            'id': node.id,
            'title': node.title,
            'content_raw': node.content_raw,
            'content_processed': node.content_processed,
            'embedding_status': node.embedding_status,
        } for node in nodes[:10]]
        return JsonResponse({'nodes': data})

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_jwt, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='dispatch')
class SummarizeView(View):
    """ API endpoint to trigger summarization. """
    def post(self, request, node_id):
        try:
            node = get_object_or_404(KnowledgeBaseNode, id=node_id)
            async_to_sync(process_article_pipeline)(node.id)
            node.refresh_from_db()
            
            return JsonResponse({
                'status': 'success',
                'node': {
                    'id': node.id,
                    'content_processed': node.content_processed,
                    'embedding_status': node.embedding_status
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_jwt, name='dispatch')
class IngestView(View):
    """ API endpoint to manually trigger a news fetch. """
    def post(self, request):
        try:
            async_to_sync(trigger_news_ingestion)("AI technology breakthrough")
            return JsonResponse({'status': 'success', 'message': 'Ingestion started'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Ingestion failed'}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_jwt, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True), name='dispatch')
class GlossaryView(View):
    """ API endpoint to define a term based on the article's context. """
    def post(self, request):
        from services.ai_service import AIService
        try:
            data = json.loads(request.body)
            term = data.get('term')
            node_id = data.get('node_id')
            
            node = get_object_or_404(KnowledgeBaseNode, id=node_id)
            ai_service = AIService()
            context = node.full_text_scraped or node.content_raw
            
            definition = async_to_sync(ai_service.explain_term)(term, context)
            return JsonResponse({'status': 'success', 'definition': definition})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_jwt, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True), name='dispatch')
class AskQuestionView(View):
    """ API endpoint to answer a question based on the article's context. """
    def post(self, request):
        from services.ai_service import AIService
        try:
            data = json.loads(request.body)
            question = data.get('question')
            node_id = data.get('node_id')
            
            node = get_object_or_404(KnowledgeBaseNode, id=node_id)
            ai_service = AIService()
            context = node.full_text_scraped or node.content_processed or node.content_raw
            
            answer = async_to_sync(ai_service.answer_question)(question, context)
            return JsonResponse({'status': 'success', 'answer': answer})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

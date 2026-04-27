from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('summarize/<int:node_id>/', views.SummarizeView.as_view(), name='summarize'),
    path('ingest/', views.IngestView.as_view(), name='ingest'),
    path('glossary/', views.GlossaryView.as_view(), name='glossary'),
    path('ask/', views.AskQuestionView.as_view(), name='ask'),
]

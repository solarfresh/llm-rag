from django.urls import path

from . import views


urlpatterns = [
    path(
        'info',
        views.KnowledgeInfoView.as_view(),
        name='knowledge-info'
    ),
    path(
        '<str:knowledge_set_id>/search',
        views.KnowledgeSetQueryView.as_view(),
        name='knowledge-set-search'
    ),
    path(
        '<str:knowledge_set_id>/html',
        views.KnowdegeSetHTMLLoaderView.as_view(),
        name='knowledge-set-html'
    ),
    path(
        '<str:knowledge_set_id>/sitemap',
        views.KnowdegeSetSitemapLoaderView.as_view(),
        name='knowledge-set-sitemap'
    ),
]

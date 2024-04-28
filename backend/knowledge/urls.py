from django.urls import path

from . import views


urlpatterns = [
    path(
        'info',
        views.KnowledgeInfoView.as_view(),
        name='knowledge-info'
    )
]

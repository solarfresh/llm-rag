from django.urls import path

from . import views


urlpatterns = [
    path(
        'completion',
        views.LLMCompletionView.as_view(),
        name='llm-completion'
    )
]

from django.urls import path

from . import views


urlpatterns = [
    path(
        'completion',
        views.LLMCompletionView.as_view(),
        name='llm-completion'
    ),
    path(
        'chatcompletion',
        views.LLMChatCompletionView.as_view(),
        name='llm-chat-completion'
    ),
]

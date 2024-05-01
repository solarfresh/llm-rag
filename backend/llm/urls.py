from django.urls import path

from . import views


urlpatterns = [
    path(
        'inference',
        views.LLMInferenceView.as_view(),
        name='llm-inference'
    )
]

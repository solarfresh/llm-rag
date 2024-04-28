from django.urls import path

from . import views


urlpatterns = [
    path(
        'readness',
        views.HealthCheckView.as_view(),
        name='healthcheck-readness'),
]

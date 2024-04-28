import uuid

from django.db import models
from django.utils import timezone as datetime
from django.utils.translation import gettext_lazy as _


class KnowledgeSetModel(models.Model):

    knowledge_set_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=64,
        null=False
    )
    description = models.TextField(null=True)
    create_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(blank=True, null=True)

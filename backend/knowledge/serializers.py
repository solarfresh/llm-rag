import uuid
from datetime import datetime
from rest_framework import serializers


class KnowledgeInfoSerializers(serializers.Serializer):
    knowledge_set_id = serializers.UUIDField(
        allow_null=True, required=False
    )
    name = serializers.CharField(
        max_length=64,
        allow_blank=False
    )
    description = serializers.CharField(allow_blank=True)
    create_at = serializers.DateTimeField(required=False)
    modified_at = serializers.DateTimeField(required=False)

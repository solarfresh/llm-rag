from rest_framework import serializers

from . import models


class KnowledgeInfoSerializers(serializers.Serializer):
    knowledge_set_id = serializers.UUIDField(
        allow_null=True, required=False
    )
    name = serializers.CharField(
        max_length=64,
        allow_blank=False
    )
    description = serializers.CharField(required=False)
    create_at = serializers.DateTimeField(required=False)
    modified_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        # document = models.KnowledgeSetDocument(knowledge_set_id)
        # call_command('opensearch', 'index', 'create', '--force')

        return models.KnowledgeInfoModel.objects.create(**validated_data)

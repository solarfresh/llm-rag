import uuid

from django.core.management import call_command
from django.db import models
from django_opensearch_dsl import Document
from django_opensearch_dsl import fields as documents
from django_opensearch_dsl.registries import registry
from django.utils import timezone as datetime
from django.utils.translation import gettext_lazy as _
from opensearchpy.helpers import field as documents_helpers


class VectorField(
    documents.DODField,
    documents_helpers.Field
):
    name = "knn_vector"

    def __init__(self, attr=None, **kwargs) -> None:
        kwargs["multi"] = True
        super(VectorField, self).__init__(attr=attr, **kwargs)


class KnowledgeSetDocument:

    def __new__(cls, index_name):
        return cls.generate_document_class(index_name)

    @classmethod
    def generate_document_class(self, index_name):
        class KnowledgeSetModel(models.Model):
            document_id = models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                editable=False
            )

            class Meta:
                managed = False

        @registry.register_document
        class KnowledgeSetDocumentTemplate(Document):
            text = documents.TextField()
            embedding = VectorField(
                dimension = 796,
                method = {
                    "name": "hnsw",
                    "space_type": "l2",
                    "engine": "lucene",
                    "parameters": {
                        "ef_construction": 128,
                        "m": 24
                    }
                }
            )

            class Django:
                model = KnowledgeSetModel

            class Index:
                name = index_name

        return KnowledgeSetDocumentTemplate


class KnowledgeInfoModel(models.Model):

    class OpenSearchManager(models.Manager):
        def create(self, **kwargs):
            instance = super().create(**kwargs)
            _ = KnowledgeSetDocument(str(instance.knowledge_set_id))
            call_command('opensearch', 'index', 'create', '--force')
            return instance

    objects = OpenSearchManager()
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

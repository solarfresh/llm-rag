from django.conf import settings
from langchain_community.vectorstores.opensearch_vector_search import OpenSearchVectorSearch
from rest_framework import generics, status
from rest_framework.response import Response

from . import models, serializers
from .tasks import celery_task as ap
from utils.embeddings import embedding


class KnowledgeInfoView(
    generics.ListCreateAPIView,
    generics.GenericAPIView
):
    queryset = models.KnowledgeInfoModel.objects.all()
    model = models.KnowledgeInfoModel
    serializer_class = serializers.KnowledgeInfoSerializers


class KnowledgeSetQueryView(
    generics.GenericAPIView
):

    def post(self, request, *args, **kwargs):
        knowledge_set_id = kwargs.get('knowledge_set_id')
        query = request.data.get('query', '')
        score_threshold = float(request.data.get('score_threshold', 0.0))
        if not query:
            return Response({
                "message": "the parameter query is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        limit = int(request.data.get('limit', 5))
        opensearch_url = settings.OPENSEARCH_DSL.get('default').get('hosts')

        vector_store = OpenSearchVectorSearch(
            opensearch_url=opensearch_url,
            index_name=knowledge_set_id,
            embedding_function=embedding
        )
        documents = vector_store.similarity_search_with_score(
            query=query,
            k=limit,
            score_threshold=score_threshold
        )

        return Response(
            {
                'results': [
                    {
                        'page_content': doc[0].page_content,
                        'score': doc[1]
                    } for doc in documents
                ],
            },
            status=status.HTTP_200_OK
        )

class KnowdegeSetHTMLLoaderView(
    generics.GenericAPIView
):

    def post(self, request, *args, **kwargs):
        knowledge_set_id = kwargs.get('knowledge_set_id')
        urls = request.data.get('urls', None)
        if urls is None:
            return Response({
                "message": "urls can not be empty."
            }, status=status.HTTP_400_BAD_REQUEST)

        ap.tasks['html_loader_task'].apply_async(
            kwargs={
                'knowledge_set_id': knowledge_set_id,
                'urls': urls
            }
        )

        return Response({}, status=status.HTTP_201_CREATED)


class KnowdegeSetSitemapLoaderView(
    generics.GenericAPIView
):

    def post(self, request, *args, **kwargs):
        knowledge_set_id = kwargs.get('knowledge_set_id')
        domain = request.data.get('domain', None)
        if domain is None:
            return Response({
                "message": "domain can not be empty."
            }, status=status.HTTP_400_BAD_REQUEST)

        ap.tasks['html_sitemap_loader_task'].apply_async(
            kwargs={
                'knowledge_set_id': knowledge_set_id,
                'domain': domain
            }
        )

        return Response({}, status=status.HTTP_201_CREATED)

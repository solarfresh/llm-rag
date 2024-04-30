import logging

from django.conf import settings
from langchain_community.document_loaders.url import UnstructuredURLLoader
from langchain_community.vectorstores.opensearch_vector_search import OpenSearchVectorSearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rest_framework import generics, status
from rest_framework.response import Response

from . import models, serializers


class KnowledgeInfoView(
    generics.ListCreateAPIView,
    generics.GenericAPIView
):
    queryset = models.KnowledgeInfoModel.objects.all()
    model = models.KnowledgeInfoModel
    serializer_class = serializers.KnowledgeInfoSerializers


class KnowdegeSetHTMLLoaderView(
    generics.CreateAPIView,
    generics.GenericAPIView
):

    def post(self, request, *args, **kwargs):
        urls = request.data.get('urls', None)
        knowledge_set_id = kwargs.get('knowledge_set_id')
        if urls is None:
            return Response({
                "message": "urls can not be empty."
            }, status=status.HTTP_400_BAD_REQUEST)

        loader = UnstructuredURLLoader(urls=urls)
        data = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )
        documents = splitter.split_documents(data)

        opensearch_url = settings.OPENSEARCH_DSL.get('default').get('hosts')

        # OpenSearchVectorSearch.from_documents(
        #     documents=documents,
        #     embedding=None,
        #     opensearch_url=opensearch_url,
        #     index_name=knowledge_set_id
        # )

        return Response([
            {
                "page_content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in documents
        ], status=status.HTTP_200_OK)

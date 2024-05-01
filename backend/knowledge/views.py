from rest_framework import generics, status
from rest_framework.response import Response

from . import models, serializers
from .tasks import celery_task as ap


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

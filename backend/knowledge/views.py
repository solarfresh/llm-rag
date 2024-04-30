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
        urls = request.data.get('url', None)
        if urls is None:
            return Response({
                "message": "urls can not be empty."
            }, status=status.HTTP_400_BAD_REQUEST)

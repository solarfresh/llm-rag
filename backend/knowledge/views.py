from rest_framework import generics

from . import models, serializers


class KnowledgeInfoView(
    generics.ListAPIView,
    generics.GenericAPIView
):
    queryset = models.KnowledgeInfoModel.objects.all()
    model = models.KnowledgeInfoModel
    serializer_class = serializers.KnowledgeInfoSerializers

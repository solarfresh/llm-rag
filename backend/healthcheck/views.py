from rest_framework import generics, status
from rest_framework.response import Response


class HealthCheckView(
    generics.GenericAPIView
):

    def get(self, request, *args, **kwargs):
        return Response('OK', status=status.HTTP_200_OK)

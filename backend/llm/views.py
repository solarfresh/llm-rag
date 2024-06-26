from rest_framework import generics, status
from rest_framework.response import Response

from utils.llms import llm


class LLMCompletionView(
    generics.GenericAPIView
):

    def post(self, request, *args, **kwargs):
        messages = request.data.get('messages', [])
        if not messages:
            return Response(
                {
                    "message": "the parameter messages is required."
                },
                status=status.HTTP_400_BAD_REQUEST)

        llm_response = llm(messages)

        return Response(
            {'result': llm_response},
            status=status.HTTP_200_OK
        )

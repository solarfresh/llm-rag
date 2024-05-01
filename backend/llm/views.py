from rest_framework import generics, status
from rest_framework.response import Response

from utils.llms import llm


class LLMInferenceView(
    generics.GenericAPIView
):

    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt', '')
        if not prompt:
            return Response(
                {
                    "message": "the parameter prompt is required."
                },
                status=status.HTTP_400_BAD_REQUEST)

        llm_response = llm(prompt)

        return Response(
            {'inference': llm_response},
            status=status.HTTP_200_OK
        )

from langchain.prompts import ChatPromptTemplate, PromptTemplate
from rest_framework import generics, status
from rest_framework.response import Response

from utils.llms import llm


class LLMCompletionView(
    generics.GenericAPIView
):

    def post(self, request, *args, **kwargs):
        template = request.data.get('template', [])
        input_variables = request.data.get('input_variables', {})
        if not template:
            return Response(
                {
                    "message": "the parameter template is required."
                },
                status=status.HTTP_400_BAD_REQUEST)

        prompt_template = PromptTemplate.from_template(template)
        llm_response = llm(prompt_template.format(**input_variables))

        return Response(
            {'result': llm_response},
            status=status.HTTP_200_OK
        )


class LLMChatCompletionView(
    generics.GenericAPIView
):

    def post(self, request, *args, **kwargs):
        chat_template = request.data.get('chat_template', '')
        input_variables = request.data.get('input_variables', {})
        if not chat_template:
            return Response(
                {
                    "message": "the parameter chat_template is required."
                },
                status=status.HTTP_400_BAD_REQUEST)

        chat_template = ChatPromptTemplate.from_messages(chat_template)
        chat_chain = chat_template | llm
        llm_response = chat_chain.invoke(input_variables)

        return Response(
            {'result': llm_response},
            status=status.HTTP_200_OK
        )

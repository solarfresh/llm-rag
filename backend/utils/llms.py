from typing import Any

from django.conf import settings
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_openai import AzureOpenAI, AzureChatOpenAI
from langchain_google_vertexai import VertexAIModelGarden
from transformers import pipeline


class VertexAIModelGardenWrapper:

    def __init__(self, vertexai_model):
        self.vertexai_model = vertexai_model

    def invoke(self, prompt):
        return self.vertexai_model(
            prompt=prompt
        )

class LargeLanguageModels:
    def __new__(cls, platform) -> Any:
        if platform == 'azure':
            return AzureOpenAI(
                deployment_name=settings.AZURE_OPENAI_LARGE_LANGUAGE_MODEL,
                max_tokens=2048
            ).invoke
        elif platform == 'azurechat':
            return AzureChatOpenAI(
                deployment_name=settings.AZURE_OPENAI_LARGE_LANGUAGE_MODEL,
                max_tokens=2048
            ).invoke
        elif platform == 'vertexai':
            return cls.build_vertexai_model()
        elif platform == 'hf':
            return cls.build_hf_model()
        else:
            return None

    @classmethod
    def build_vertexai_model(cls):
        vertexai_model = VertexAIModelGarden(
            endpoint_id=settings.VERTEXAI_LARGE_LANGUAGE_MODEL_ENDPOINT,
            project=settings.GCP_PROJECT_ID,
            allowed_model_args=[
                "temperature",
                "max_tokens",
                "top_p",
                "top_k",
                "raw_response"
            ]
        )

        return VertexAIModelGardenWrapper(
            vertexai_model=vertexai_model
        ).invoke

    @classmethod
    def build_hf_model(cls):
        import torch

        if settings.HUGGINGFACE_LARGE_LANGUAGE_MODEL is None:
            return None

        pipe = pipeline(
            "text-generation",
            model=settings.HUGGINGFACE_LARGE_LANGUAGE_MODEL,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
        )

        return HuggingFacePipeline(pipeline=pipe)


class LargeLanguageModelsStream:
    def __new__(cls, platform) -> Any:
        if platform == 'azurechat':
            return AzureChatOpenAI(
                deployment_name=settings.AZURE_OPENAI_LARGE_LANGUAGE_MODEL,
                max_tokens=2048,
                streaming=True
            ).stream
        else:
            return None

llm = LargeLanguageModels(platform=settings.LARGE_LANGUAGE_MODEL_PLATFORM)
llm_stream = LargeLanguageModelsStream(
    platform=settings.LARGE_LANGUAGE_MODEL_PLATFORM)

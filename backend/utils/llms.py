from typing import Any

import openai
from django.conf import settings
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_openai import AzureOpenAI
from transformers import pipeline


class LargeLanguageModels:
    def __new__(cls, platform) -> Any:
        if platform == 'azure':
            return AzureOpenAI(
                client=openai.ChatCompletion(),
                deployment_name=settings.AZURE_OPENAI_LARGE_LANGUAGE_MODEL
            ).invoke
        elif platform == 'hf':
            return cls.build_hf_model()
        else:
            return None

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


llm = LargeLanguageModels(platform=settings.LARGE_LANGUAGE_MODEL_PLATFORM)

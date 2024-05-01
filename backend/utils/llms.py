from typing import Any

from django.conf import settings
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import pipeline


class LargeLanguageModels:
    def __new__(cls, platform) -> Any:
        if platform == 'hf':
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
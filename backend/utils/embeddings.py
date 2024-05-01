from typing import Any

from django.conf import settings
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from openai import embeddings


class Embeddings:
    def __new__(cls, platform) -> Any:
        if platform == 'azure':
            return AzureOpenAIEmbeddings(
                model=settings.AZURE_OPENAI_EMBEDDING_MODEL)
        elif platform == 'hf':
            return HuggingFaceEmbeddings(
                model_name=settings.HUGGINGFACE_EMBEDDING_MODEL,
                model_kwargs=settings.HUGGINGFACE_EMBEDDING_MODEL_CONFIG
            )
        else:
            return None


embedding = Embeddings(platform=settings.EMBEDDINGS_PLATFORM)

import logging

from typing import List

from config.celery_app import celery_task
from django.conf import settings

from langchain_community.document_loaders.url import UnstructuredURLLoader
from langchain_community.vectorstores.opensearch_vector_search import OpenSearchVectorSearch
from langchain_text_splitters import RecursiveCharacterTextSplitter


class HTMLLoaderTask(celery_task.Task):

    name = 'html_loader_task'

    def run(self, knowledge_set_id: str, urls: List[str]):
        loader = UnstructuredURLLoader(urls=urls)
        data = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )
        documents = splitter.split_documents(data)

        opensearch_url = settings.OPENSEARCH_DSL.get('default').get('hosts')

        # OpenSearchVectorSearch.from_documents(
        #     documents=documents,
        #     embedding=None,
        #     opensearch_url=opensearch_url,
        #     index_name=knowledge_set_id
        # )

        for doc in documents:
            logging.info('=================')
            logging.info(doc.page_content)


task_classes = [
    HTMLLoaderTask,
]

for task_class in task_classes:
    celery_task.register_task(task_class)

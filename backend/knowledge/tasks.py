import logging
import requests
from urllib.parse import urlparse, urljoin
from typing import List

from bs4 import BeautifulSoup
from config.celery_app import celery_task
from django.conf import settings
from langchain_community.document_loaders.url import UnstructuredURLLoader
from langchain_community.vectorstores.opensearch_vector_search import OpenSearchVectorSearch
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.embeddings import embedding


class HTMLLoaderTask(celery_task.Task):

    name = 'html_loader_task'

    def run(self, knowledge_set_id: str, urls: List[str]):
        if embedding is None:
            return None

        logging.info('start to parse webpages...')
        loader = UnstructuredURLLoader(urls=urls)
        data = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )
        documents = splitter.split_documents(data)

        opensearch_url = settings.OPENSEARCH_DSL.get('default').get('hosts')

        logging.info('start to load documents to a vector db...')
        OpenSearchVectorSearch.from_documents(
            documents=documents,
            embedding=embedding,
            opensearch_url=opensearch_url,
            index_name=knowledge_set_id
        )
        logging.info('end of loading documents to a vector db...')


class HTMLSitemapLoaderTask(celery_task.Task):

    name = 'html_sitemap_loader_task'

    def run(self, knowledge_set_id: str, domain: str):
        if embedding is None:
            return None

        logging.info('start to parse webpages...')
        urls = list(self.get_urls(domain=domain))
        loader = UnstructuredURLLoader(urls=urls)
        data = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0
        )
        documents = splitter.split_documents(data)

        opensearch_url = settings.OPENSEARCH_DSL.get('default').get('hosts')

        logging.info('start to load documents to a vector db...')
        OpenSearchVectorSearch.from_documents(
            documents=documents,
            embedding=embedding,
            opensearch_url=opensearch_url,
            index_name=knowledge_set_id
        )
        logging.info('end of loading documents to a vector db...')

    def get_links(self, domain, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for link in soup.find_all('a'):
            link_url = link.get('href')
            if link_url:
                absolute_link = urljoin(url, link_url)
                links.add(absolute_link)

        return links

    def get_urls(self, domain):
        queue = [domain]
        visited = set()

        while queue:
            url = queue.pop(0)
            visited.add(url)
            links = self.get_links(domain, url)
            for link in links:
                if link not in visited and link not in queue:
                    queue.append(link)

        return visited


task_classes = [
    HTMLLoaderTask,
    HTMLSitemapLoaderTask
]

for task_class in task_classes:
    celery_task.register_task(task_class)

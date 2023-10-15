from http import HTTPStatus
from typing import Dict, List, Optional
from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.exceptions import ConnectionError
from fastapi import HTTPException

from db.base import DatabaseModel
from core.decorators import backoff

connection: Optional[AsyncElasticsearch] = None


async def get_elastic() -> AsyncElasticsearch:
    """
    Get an Elasticsearch connection instance, which will be used for dependency injection.

    Returns:
        AsyncElasticsearch: Connection to Elasticsearch
    """
    return connection


class ElasticStorage(DatabaseModel):
    """Class for working with Elasticsearch storage as the primary database."""

    elastic: AsyncElasticsearch

    @backoff(errors=(ConnectionError))
    async def get_elastic_doc(self, index: str, doc_id: UUID) -> Dict:
        """
        Get a document from Elasticsearch.

        Args:
            index: Index with documents
            doc_id: Document ID

        Raises:
            HTTPException: If the document doesn't exist, return an HTTP 404 status.

        Returns:
            Dict: Document data without information about the request results
        """
        try:
            doc = await self.elastic.get(index=index, id=doc_id)
        except NotFoundError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        return doc['_source']

    @backoff(errors=(ConnectionError))
    async def search_elastic_docs(self, index: str, queryset: Optional[Dict] = None) -> List[Dict]:
        """
        Get a list of documents from Elasticsearch.

        Args:
            index: Index with documents
            queryset: Query parameters for searching data

        Raises:
            HTTPException: If there are no documents for the query, return an HTTP 404 status.

        Returns:
            List[dict]: List of document data without information about the request results
        """
        try:
            docs = await self.elastic.search(index=index, **queryset or {})
        except NotFoundError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        return [doc['_source'] for doc in docs['hits']['hits']]

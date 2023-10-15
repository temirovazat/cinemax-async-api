from typing import List, Type

from services.base import BaseService, redis_cache
from services.mixins import QuerysetMixin, SingleObjectMixin
from core.config import CONFIG, CinemaObject, CinemaObjectList


class ListService(BaseService, SingleObjectMixin, QuerysetMixin):
    """Service for representing a list of cinema objects."""

    model: Type[CinemaObjectList]

    @property
    def redis_key(self) -> str:
        """
        Key for data in the Redis cache in the form of an index and query parameters in the URL.

        Returns:
            str: Index and parameters separated by colons
        """
        params = [
            f'{field}::{value}' for field, value in self.__repr_args__()
            if field in {'filter', 'page_number', 'page_size', 'query', 'sort'}
        ]
        return '{index}::{params}'.format(index=self.index, params='::'.join(params))

    @redis_cache(expire=CONFIG.fastapi.cache_expire_in_seconds)
    async def get(self) -> List[CinemaObject]:
        """
        Retrieve a list of cinema objects.

        Returns:
            List[CinemaObject]: List of cinema objects
        """
        queryset = await self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        data = await self.search_elastic_docs(self.index, page)
        obj_list = [
            await self.get_object(item, self.model.item) for item in data
        ]
        return obj_list

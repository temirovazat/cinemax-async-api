from typing import Optional, Type
from uuid import UUID

from services.base import BaseService, redis_cache
from services.mixins import SingleObjectMixin
from core.config import CONFIG, CinemaObject


class RetrieveService(BaseService, SingleObjectMixin):
    """Service for retrieving a cinema object by ID."""

    model: Type[CinemaObject]
    id: Optional[UUID]

    @property
    def redis_key(self) -> str:
        """
        Get the key for data in the Redis cache in the format of index and the ID of the requested document.

        Returns:
            str: Index and ID separated by colons
        """
        return '{index}::id::{id}'.format(index=self.index, id=self.id)

    @redis_cache(expire=CONFIG.fastapi.cache_expire_in_seconds)
    async def get(self) -> CinemaObject:
        """
        Retrieve a single cinema object.

        Returns:
            CinemaObject: The cinema object
        """
        data = await self.get_elastic_doc(self.index, self.id)
        obj = await self.get_object(data, self.model)
        return obj

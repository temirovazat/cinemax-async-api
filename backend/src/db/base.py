from pydantic import BaseModel


class DatabaseModel(BaseModel):
    """Base class for working with the storage."""

    class Config:
        """Validation settings."""

        arbitrary_types_allowed = True

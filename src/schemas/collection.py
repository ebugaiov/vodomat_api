from pydantic import BaseModel

from .status import StatusSchema


class CollectionsSchema(BaseModel):
    collections: list[StatusSchema]
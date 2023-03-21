from enum import Enum
from pydantic import BaseModel


class MediaType(str, Enum):
    ANIME = "anime"
    MANGA = "manga"


class Item(BaseModel):
    item_id: int
    title: str
    media_type: MediaType

    # https://stackoverflow.com/a/65211727
    class Config:
        use_enum_values = True

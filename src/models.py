from pydantic import BaseModel


class Item(BaseModel):
    item_id: int
    title: str
    rating: float

import pickle

import pandas as pd

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


class Recommender():
    SAMPLE_WEIGHTS_PATH = 'assets/sample-weights.pkl'
    SAMPLE_USERS_PATH = 'assets/sample_users.parquet'
    ITEMS_INDEX_PATH = 'assets/items_index.parquet'

    def __init__(self):
        with open(self.SAMPLE_WEIGHTS_PATH, 'rb') as f:
            self.model = pickle.load(f)
        self.items_index = pd.read_parquet(self.ITEMS_INDEX_PATH)
        self.sample_users = pd.read_parquet(self.SAMPLE_USERS_PATH)

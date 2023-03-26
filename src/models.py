import pickle
from enum import Enum

import pandas as pd
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


class FavoriteType(str, Enum):
    ANIME = "anime"
    MANGA = "manga"
    CHARACTERS = "characters"
    PEOPLE = "people"


class Favorite(BaseModel):
    title: str
    fav_type: FavoriteType

    class Config:
        use_enum_values = True


class Recommender():
    WEIGHTS_PATH = 'assets/weights.pkl'
    USERS_PATH = 'assets/users.parquet'
    ITEMS_INDEX_PATH = 'assets/items_index.parquet'

    def __init__(self):
        with open(self.WEIGHTS_PATH, 'rb') as f:
            self.model = pickle.load(f)
        self.items_index = pd.read_parquet(self.ITEMS_INDEX_PATH)
        self.users = pd.read_parquet(self.USERS_PATH)

class AssociationRules():
    FAVS_PATH = 'assets/favs.parquet'
    PREDICTIONS_PATH = 'assets/predictions.parquet'

    def __init__(self):
        self._favs = pd.read_parquet(self.FAVS_PATH)  # unused
        self._predictions = pd.read_parquet(self.PREDICTIONS_PATH)

    def get_predictions(self, user_id: int) -> list[Favorite]:
        preds = self._predictions.query(f'user_id == {user_id}')
        return [
            Favorite(title=prediction, fav_type=fav_type)
            for fav_type, prediction in preds[['type', 'prediction']].values
        ]

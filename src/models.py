import pickle
from enum import Enum

import pandas as pd
from pydantic import BaseModel


class MediaType(str, Enum):
    ANIME = "anime"
    MANGA = "manga"


class SectionType(str, Enum):
    ANIME = "anime"
    MANGA = "manga"
    CHARACTERS = "characters"
    PEOPLE = "people"


class Item(BaseModel):
    item_id: int
    title: str
    media_type: MediaType

    # https://stackoverflow.com/a/65211727
    class Config:
        use_enum_values = True


class Favorite(BaseModel):
    title: str
    fav_type: SectionType

    class Config:
        use_enum_values = True


class Rule(BaseModel):
    found_item: str
    pairs: list[str]  # could've be Item, but need to facilitate item_id lookup
    recs: str
    conf: float
    supp: float
    lift: float


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
    RULES_DIR_PATH = 'assets/rules'

    def __init__(self):
        self._favs = pd.read_parquet(self.FAVS_PATH)  # ! unused
        self._predictions = pd.read_parquet(self.PREDICTIONS_PATH)

    def get_predictions(self, user_id: int) -> list[Favorite]:
        preds = self._predictions.query(f'user_id == {user_id}')
        return [
            Favorite(title=prediction, fav_type=fav_type)
            for fav_type, prediction in preds[['type', 'prediction']].values
        ]

    def get_rules(self, section: SectionType, query: str) -> list[Rule]:
        lowercased_query = query.lower()

        # load data
        rules = pd.read_excel(f"{self.RULES_DIR_PATH}/{section}__rules.xlsx", engine="openpyxl")

        # make sure the antecedent is in lowercase to facilitate searching
        rules['lowercase_antecedent'] = rules.antecedent.str.lower()

        # sort descending
        rules = rules.sort_values(['confidence', 'support', 'lift'], ascending=False)

        # search
        found_query = rules.loc[
            rules.lowercase_antecedent.str.contains(lowercased_query), [
                'antecedent', 'consequent', 'lowercase_antecedent', 'confidence',
                'support', 'lift'
            ]]  # reorder the columns

		# if query not found
        if found_query.shape[0] == 0:
            return []

		# if query found...
        results: list[Rule] = []
        found_item: str = ""
        for index, (ante, cons, lc_ante, conf, supp,
                    lift) in zip(found_query.index, found_query.values):
            # ! unused index. could be used to lookup item_id
            pairs = []

            ante_ = eval(ante)
            cons_ = eval(cons)[0]  # one entry inside a list
            l_ante_ = eval(lc_ante)

			# loop through antecedents
            for item, item_for_search in zip(ante_, l_ante_):
                # search in l_ante_, but append ante_
                if lowercased_query in item_for_search:
                    found_item = item
                    continue
                else:
                    pairs.append(item)

            results.append(
                Rule(
                    found_item=found_item,
                    pairs=pairs,
                    recs=cons_,
                    conf=conf,
                    supp=supp,
                    lift=lift
                )
            )

        return results

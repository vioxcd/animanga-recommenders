import pickle
from src.models import Item, MediaType
from functools import partial

import numpy as np
import pandas as pd


def _post_rank(user_id, recs, df):
    '''Final recommendation list for the user, based on `unseen items recommendation`'''
    f = df.user == user_id  # filter current user from df
    seen_items = df.loc[f]['item'].values  # get current user seen items
    recs = set(recs.index)
    return list(recs.difference(seen_items))  # take only unseen items


def _topk_rank(user_id, k, item_type, crm, items_index, df):
    '''Recommend top K items of certain type based on the computed rating matrix

    Parameters
    ----------
    user_id     : int. the user's ID
    k           : int. number of items to recommend
    item_type   : str. either anime or manga
    crm         : ndarray. the computex matrix
    items_index : dataframe. a dataframe with `item` index and `title` column
    df          : dataframe. the whole user-item dataframe
    '''
    assert user_id >= 0 and user_id < crm.shape[0]
    assert k >= 0
    assert item_type in ('anime', 'manga')

    # get ratings
    ratings = crm[user_id]

    # generate ranking
    ranking = np.argpartition(ratings, -k)[-k:]
    sorted_ranking = ranking[np.argsort(
        ratings[ranking])][::-1]  # -1 for descending

    # generate recommendations. sorted and filtered by `type`
    recs = items_index.iloc[sorted_ranking].copy()
    recs = recs.loc[recs['type'] == item_type]

    # post_rank: only recommend unseen items
    unseen_items = _post_rank(user_id, recs, df)
    return items_index.iloc[unseen_items]


def get_recommended_items(user_id: int, media_type: MediaType,
                          k: int) -> list[Item]:
    SAMPLE_WEIGHTS_PATH = 'assets/sample-weights.pkl'
    SAMPLE_USERS_PATH = 'assets/sample_users.parquet'
    ITEMS_INDEX_PATH = 'assets/items_index.parquet'

    with open(SAMPLE_WEIGHTS_PATH, 'rb') as f:
        model = pickle.load(f)
    items_index = pd.read_parquet(ITEMS_INDEX_PATH)
    sample_users = pd.read_parquet(SAMPLE_USERS_PATH)

    # personal note: topk_rank could be used flexibly based on k
    topk_rank = partial(_topk_rank,
                        crm=model,
                        items_index=items_index,
                        df=sample_users)
    recs = topk_rank(user_id, k, media_type)

    return [
        Item(item_id=item_id, title=title, media_type=media_type)
        for item_id, (_, title) in recs.iterrows()
    ]

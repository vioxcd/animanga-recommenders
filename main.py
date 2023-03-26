from fastapi import FastAPI, HTTPException

from src.models import (AssociationRules, Favorite, Item, MediaType,
                        Recommender, Rule, SectionType)
from src.recommendations import get_recommended_items

app = FastAPI(title="Animanga Recommenders")

USERS_COUNT = 4


@app.on_event("startup")
def load_recommender():
    # Load recommender
    global recommender
    global association_rules
    recommender = Recommender()
    association_rules = AssociationRules()


@app.get("/recs/{user_id}/")
async def get_recommendations(user_id: int,
                              media_type: MediaType = MediaType.MANGA,
                              k: int = 100) -> list[Item]:

    # as currently the app samples 4 users,
    # throw error if given `user_id` is equal or more than 4
    if user_id >= USERS_COUNT:
        raise HTTPException(status_code=404,
                            detail="user_id can only be between 0 to 3")

    items = get_recommended_items(user_id, media_type, k, recommender)
    return items


@app.get("/favs_assoc/{user_id}/")
async def get_favorites_predictions(user_id: int) -> list[Favorite]:

    if user_id >= USERS_COUNT:
        raise HTTPException(status_code=404,
                            detail="user_id can only be between 0 to 3")

    items = association_rules.get_predictions(user_id)
    return items

@app.get("/search_rules/{section}/")
async def search_rules(section: SectionType, query: str) -> list[Rule]:

	# there's anime with title length as short as 2 (e.g. 86), so imposing limit
    # for possible query would be hard to do. but, at least, all query shouldn't
    # be an empty string
    if query == "":
        raise HTTPException(status_code=404,
                            detail="query should not be an empty string")
    rules = association_rules.get_rules(section, query)
    return rules

from fastapi import FastAPI

app = FastAPI()

from src.models import Item, MediaType
from src.recommendations import get_recommended_items


@app.get("/{user_id}/")
async def get_recommendations(user_id: int,
                              media_type: MediaType = MediaType.MANGA,
                              k: int = 100) -> list[Item]:
    items = get_recommended_items(user_id, media_type, k)
    return [item.dict() for item in items]

from fastapi import FastAPI

app = FastAPI()

from src.models import Item
from src.recommendations import get_recommended_items


@app.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int) -> list[Item]:
    items = get_recommended_items(user_id)
    return [item.dict() for item in items]

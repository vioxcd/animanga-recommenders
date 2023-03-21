import pickle
from src.models import Item


def get_recommended_items(user_id: int) -> list[Item]:
    return [
        Item(item_id=20357, title="Shingeki no Kyojin", rating=9.0),
        Item(item_id=12345, title="Houseki no Kuni", rating=10.0),
    ]


with open('sample-weights.pkl', 'rb') as f:
    model = pickle.load(f)

print(model)
print(type(model))
print(model.shape)

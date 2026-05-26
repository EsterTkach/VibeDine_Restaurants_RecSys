from src import config
import pandas as pd
import pickle
import os
from scipy.sparse import csr_matrix

### load data
interactions = pd.read_parquet(config.INTERACTIONS_FILE)
restaurants = pd.read_parquet(config.CBF_FEATURES_FILE)
restaurant_lookup = restaurants.set_index("gmap_id")[["name"]]

print("Data loaded successfully")

interactions = interactions[interactions["rating"] >= config.MIN_RATING]

# encode users/items to numeric indices
user_categories = interactions["user_id"].astype("category")
item_categories = interactions["gmap_id"].astype("category")

user_indices = user_categories.cat.codes
item_indices = item_categories.cat.codes

# sparse user-item matrix
user_item_matrix = csr_matrix(
    (
        interactions["rating"].astype(float),
        (user_indices, item_indices),
    )
)

# sparse item-user matrix
item_user_matrix = user_item_matrix.T.tocsr()

# mappings
user_id_to_index = dict(
    zip(user_categories.cat.categories, range(len(user_categories.cat.categories)))
)

item_id_to_index = dict(
    zip(item_categories.cat.categories, range(len(item_categories.cat.categories)))
)

index_to_item_id = dict(enumerate(item_categories.cat.categories))

os.makedirs("models", exist_ok=True)

with open(config.MODEL_CF_FILE, "wb") as f:
    pickle.dump(
        {
            "user_item_matrix": user_item_matrix,  # users × restaurants matrix
            "item_user_matrix": item_user_matrix,  # restaurants × users matrix
            "user_id_to_index": user_id_to_index,  # user_id -> index
            "item_id_to_index": item_id_to_index,  # gmap_id -> index
            "index_to_item_id": index_to_item_id,  # index -> gmap_id
            "restaurant_lookup": restaurant_lookup,
        },
        f,
    )

print("Sparse Item-Based CF model saved")

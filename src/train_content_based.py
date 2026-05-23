from src import config
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

### load data
restaurants = pd.read_parquet(config.CBF_FEATURES_FILE)
restaurants = restaurants.reset_index(drop=True)

print("Data loaded successfully")


### clean data for combined_text
def clean_text(values):
    if isinstance(values, list):  # flatten in case of list of str
        return " ".join(map(str, values))

    if pd.isna(values):
        return ""

    if str(values).strip() == "-":
        return ""

    return str(values)


text_columns = {
    "name": "name_text",
    "category": "category_text",
    "service_options": "service_text",
    "dining_options": "dining_text",
}

for source_col, target_col in text_columns.items():
    restaurants[target_col] = restaurants[source_col].apply(clean_text)


### create combined text Features column
restaurants["combined_text"] = (
    restaurants["name_text"]
    + " "
    + restaurants["category_text"]
    + " "
    + restaurants["service_text"]
    + " "
    + restaurants["dining_text"]
)


print("Combined text created")


### TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words="english", max_features=config.MAX_FEATURES)

tfidf_matrix = tfidf.fit_transform(restaurants["combined_text"])

print("TF-IDF matrix created")


### save model
os.makedirs("models", exist_ok=True)

with open(config.MODEL_CB_FILE, "wb") as f:
    pickle.dump(
        {
            "restaurants": restaurants,
            "tfidf": tfidf,
            "tfidf_matrix": tfidf_matrix,
        },
        f,
    )

print("Model saved to models/content_based_model.pkl")

from pathlib import Path

# This gets the directory where config.py lives (src/) and goes up one level to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_PATH = BASE_DIR / "data"
MODEL_PATH = BASE_DIR / "models"

DATA_VERSION = "2"

# Content-Based parameters
MAX_FEATURES = 10000

# Recommendation settings
TOP_K = 10
MIN_RATING = 4

# Files
CBF_FEATURES_FILE = f"{DATA_PATH}/CBF_item_features_{DATA_VERSION}.parquet"
INTERACTIONS_FILE = f"{DATA_PATH}/CF_interaction_matrix_{DATA_VERSION}.parquet"
MODEL_CB_FILE = f"{MODEL_PATH}/content_based_model.pkl"
MODEL_CF_FILE = f"{MODEL_PATH}/item_cf_model.pkl"

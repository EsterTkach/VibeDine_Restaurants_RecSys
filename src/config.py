# Paths
DATA_PATH = "data/"
MODEL_PATH = "models/"

# Content-Based parameters
MAX_FEATURES = 10000

# Recommendation settings
TOP_K = 10
MIN_RATING = 4

# Files
CBF_FEATURES_FILE = f"{DATA_PATH}CBF_item_features.parquet"
INTERACTIONS_FILE = f"{DATA_PATH}CF_interaction_matrix.parquet"
MODEL_CB_FILE = f"{MODEL_PATH}content_based_model.pkl"
MODEL_CF_FILE = f"{MODEL_PATH}item_cf_model.pkl"

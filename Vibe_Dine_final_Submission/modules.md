# Modules Description

## User Interface (Frontend)

- Technology: React 19, TypeScript, React Router v7, Tailwind CSS 4, Vite
- Responsibilities: Display personalized restaurant recommendation carousels, collect user preferences through onboarding and Vibe Matcher, handle group friend selection, and manage user auth flows.
- Interactions:
  - Calls backend APIs (`/recommend/home-carousels`, `/recommend/vibe-match`, `/groups/session`, `/users/*`).
  - Receives carousel data, group recommendations, and user profile info from backend to render UI.
- Source code: [`/frontend/src/`](../frontend/src/)

## Recommendation Engine (Hybrid System)

- Technology: scikit-learn (TF-IDF, cosine similarity, sparse CSR matrices), NumPy, pandas
- Responsibilities: Generate personalized restaurant recommendations by combining Content-Based Filtering and Collaborative Filtering with adaptive alpha weighting per user.
- Interactions:
  - Receives user likes (offline from parquet data + online from MongoDB) to compute scores.
  - Content-Based module computes TF-IDF similarity on restaurant features.
  - Collaborative Filtering module uses item-based weighted CF on the user-item interaction matrix.
  - Hybrid scores are combined: `hybrid_score = alpha × CF + (1 - alpha) × CB`, with alpha determined by user interaction count.
  - Returns ranked restaurant IDs to the routes layer.
- Source code: [`/api/services/recommendation_service.py`](../api/services/recommendation_service.py)

## Content-Based Filtering (CB)

- Technology: scikit-learn TF-IDF Vectorizer, cosine similarity
- Responsibilities: Compute similarity between restaurants based on text features (name, category, service options, dining options). Generate CB scores for a user by averaging cosine similarities across their liked items.
- Interactions:
  - Loads pre-trained TF-IDF model from `/models/content_based_model.pkl`.
  - Used by the Hybrid Recommendation Engine to supply CB scores.
- Source code: [`/api/ml/cb_recommender.py`](../api/ml/cb_recommender.py)

## Collaborative Filtering (CF)

- Technology: scikit-learn, SciPy sparse matrices, NumPy
- Responsibilities: Compute item-based collaborative filtering scores using a weighted similarity approach: `score[i] = Σ(sim[liked_j, i] × rating[j]) / Σ(sim[liked_j, i])`. Augments offline interaction matrix with online likes (rated as 5).
- Interactions:
  - Loads pre-trained CF model from `/models/item_cf_model.pkl`.
  - Queries online likes from MongoDB to augment the offline matrix.
  - Used by the Hybrid Recommendation Engine to supply CF scores.
- Source code: [`/api/ml/cf_recommender.py`](../api/ml/cf_recommender.py)

## Group Recommendation Service

- Technology: Python (concurrent.futures for parallel user processing)
- Responsibilities: Generate group-consensus restaurant recommendations by aggregating per-user hybrid scores, weighting by coverage (how many group members got that restaurant). Supports session-based feedback to iteratively refine results. Falls back to popular restaurants when no results are found.
- Interactions:
  - Calls the Hybrid Recommendation Engine for each group member in parallel.
  - Aggregates scores: `group_score = avg_score × coverage`.
  - Falls back to popular restaurants when group has only cold-start users or aggregation yields no matches.
- Source code: [`/api/services/groups_service.py`](../api/services/groups_service.py), [`/api/services/group_session_service.py`](../api/services/group_session_service.py)

## Database & Repository Layer

- Technology: MongoDB Atlas, PyMongo
- Responsibilities: Store restaurant data, user profiles, and user interactions. Provide advanced aggregation pipelines for filtered restaurant queries with tag-based scoring, geospatial radius filtering, and quality thresholds.
- Interactions:
  - Accessed by the Recommendation Engine to fetch candidate restaurant pools.
  - Accessed by user routes for auth, preferences, likes, and friends.
  - Geospatial queries require a `2dsphere` index on the `location` field.
- Source code: [`/api/db/`](../api/db/)

## API Gateway / Backend Server

- Technology: FastAPI (Python), Uvicorn
- Responsibilities: Expose REST endpoints for recommendations, user management, and group sessions. Orchestrate requests between the frontend, recommendation engine, and database.
- Interactions:
  - Handles all frontend HTTP requests.
  - Routes requests to recommendation services, user services, and group services.
  - Applies CORS middleware for frontend communication.
- Source code: [`/api/`](../api/)

## Data & Model Training Pipeline

- Technology: pandas, scikit-learn, Parquet files
- Responsibilities: Preprocess restaurant features and user interaction data, train the Content-Based (TF-IDF) and Collaborative Filtering (item-based CF) models, and export trained `.pkl` files.
- Interactions:
  - Reads `data/CBF_item_features_1.parquet` for restaurant features.
  - Reads `data/CF_interaction_matrix_1.parquet` for user-item ratings.
  - Outputs trained models to `/models/` directory.
  - `rests_uploader.py` seeds MongoDB from parquet data.
- Source code: [`/api/ml/train_content_based.py`](../api/ml/train_content_based.py), [`/api/ml/train_item_cf.py`](../api/ml/train_item_cf.py), [`/data/`](../data/)

## Enum & Constants Definitions

- Technology: Python Enum, TypeScript constants
- Responsibilities: Define the canonical set of values for restaurant attributes (cuisines, establishment types, dining styles, popular items, dietary preferences, vibes) used across backend filtering and frontend onboarding UI.
- Interactions:
  - Backend uses enums for data validation and mapping user preferences to DB queries.
  - Frontend constants mirror the enum values for onboarding option display.
- Source code: [`/enums/models_enums.py`](../enums/models_enums.py), [`/frontend/src/constants/onboardingOptions.ts`](../frontend/src/constants/onboardingOptions.ts)

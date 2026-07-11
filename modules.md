# Modules Description

## User Interface (Frontend)

- Technology: React 19, TypeScript, React Router v7, Tailwind CSS 4, Vite
- Responsibilities: Display personalized restaurant recommendation carousels, collect user preferences through onboarding and Vibe Matcher, handle group friend selection, and manage user auth flows.
- Interactions:
  - Calls backend APIs (`/recommend/home-carousels`, `/recommend/vibe-match`, `/groups/session`, `/users/*`).
  - Receives carousel data, group recommendations, and user profile info from backend to render UI.
- Source code: [`/frontend/src/`](../frontend/src/)


## Recommendation Engine (Hybrid System)

- Technology: Python, scikit-learn, NumPy, pandas
- Responsibilities: Orchestrate the recommendation process by combining Content-Based and Collaborative Filtering scores. Generate personalized recommendations for both cold-start and established users, rank candidate restaurants, and return the final results.

- Interactions:
  - Receives user interaction data from the repository layer.
  - Uses onboarding preferences for users with insufficient interaction history.
  - Requests recommendation scores from the Content-Based and Collaborative Filtering modules.
  - Combines the scores using an adaptive hybrid strategy.
  - Returns ranked restaurant recommendations to the API routes.
- Source code: [`/api/services/recommendation_service.py`](../api/services/recommendation_service.py)

## Content-Based Filtering (CB)

- Technology: scikit-learn (TF-IDF Vectorizer, cosine similarity)
- Responsibilities: Compute recommendation scores based on restaurant content similarity using textual features such as name, category, service options, and dining options.
- Interactions:
  - Loads the pre-trained TF-IDF model and restaurant feature vectors.
  - Computes Content-Based scores for the current user.
  - Returns scores to the Hybrid Recommendation Engine.
- Source code: [`/api/ml/cb_recommender.py`](../api/ml/cb_recommender.py)

## Collaborative Filtering (CF)

- Technology: scikit-learn, SciPy sparse matrices, NumPy
- Responsibilities: Compute recommendation scores using an item-based Collaborative Filtering model based on user-item interactions, while augmenting the offline interaction matrix with online user likes.
- Interactions:
  - Loads the pre-trained Collaborative Filtering model.
  - Retrieves online user interactions from MongoDB.
  - Computes Collaborative Filtering scores for the current user.
  - Returns scores to the Hybrid Recommendation Engine.
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
- Source code: [`/api/routes`](../api/)

## Data & Model Training Pipeline

- Technology: pandas, scikit-learn, Parquet files
- Responsibilities: Preprocess restaurant features and user interaction data, train the Content-Based (TF-IDF) and Collaborative Filtering (item-based CF) models, and export trained `.pkl` files.
- Interactions:
  - Reads the preprocessed restaurant feature dataset and user interaction dataset stored as Parquet files.
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

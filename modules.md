# Modules Description

## User Interface (Frontend)

- Technology: React 19, TypeScript, React Router v7, Tailwind CSS 4, Vite
- Responsibilities: Display personalized restaurant recommendation carousels, collect user preferences through onboarding and Vibe Matcher, handle group friend selection, and manage user auth flows.
- Interactions:
  - Calls backend APIs (`/recommend/home-carousels`, `/recommend/vibe-match`, `/groups/session`, `/users/*`).
  - Receives carousel data, group recommendations, and user profile info from backend to render UI.
- Source code: [`/frontend/src/`](frontend/src/)


## Recommendation Engine (Hybrid System)

- Technology: Python, scikit-learn, NumPy, pandas
- Responsibilities: 
Orchestrate the recommendation process by selecting the appropriate recommendation strategy (Cold-Start, Content-Based, or Hybrid) according to the user's interaction history. Combine Content-Based and Collaborative Filtering scores using adaptive weighting, rank candidate restaurants, and return the final recommendations.

- Interactions:
  - Receives candidate restaurants and user interaction data from the repository layer.
  - Uses onboarding preferences for users with insufficient interaction history.
  - Requests recommendation scores from the Content-Based and Collaborative Filtering modules.
  - Combines the scores using an adaptive hybrid strategy.
  - Returns ranked restaurant recommendations to the API routes.
- Source code: [`api/services/recommendation_service.py`](api/services/recommendation_service.py)

## Content-Based Filtering (CB)

- Technology: scikit-learn (TF-IDF Vectorizer, cosine similarity)
- Responsibilities: Compute Content-Based recommendation scores using restaurant metadata represented as TF-IDF vectors.
- Interactions:
  - Loads the pre-trained TF-IDF model and restaurant feature vectors.
  - Computes Content-Based scores for the current user.
  - Returns scores to the Hybrid Recommendation Engine.
- Source code: [`api/ml/cb_recommender.py`](api/ml/cb_recommender.py)

## Collaborative Filtering (CF)

- Technology: scikit-learn, SciPy sparse matrices, NumPy
- Responsibilities: Compute recommendation scores using an Item-Based Collaborative Filtering model by combining offline interaction data with online user likes.
- Interactions:
  - Loads the pre-trained Collaborative Filtering model.
  - Retrieves online user interactions from MongoDB.
  - Computes Collaborative Filtering scores for the current user.
  - Returns scores to the Hybrid Recommendation Engine.
- Source code: [`api/ml/cf_recommender.py`](api/ml/cf_recommender.py)


## Group Recommendation Service

- Technology: Python (concurrent.futures for parallel user processing)
- Responsibilities: Generate consensus recommendations by aggregating personalized hybrid recommendations for all group members. After each feedback round, update each user's candidate set, recompute recommendation scores, and generate a new group recommendation.
- Interactions:
  - Calls the Hybrid Recommendation Engine for each group member in parallel.
  - Aggregates scores: `group_score = avg_score × coverage`.
  - Falls back to popular restaurants when group has only cold-start users or aggregation yields no matches.
- Source code: [`/api/services/groups_service.py`](api/services/groups_service.py), [`/api/services/group_session_service.py`](../api/services/group_session_service.py)

## Database & Repository Layer

- Technology: MongoDB Atlas, PyMongo
- Responsibilities: 
Store runtime application data and retrieve restaurant candidates using MongoDB aggregation pipelines. Candidate retrieval supports quality filtering, geospatial filtering, user preference filtering, and relevance-based ranking.
- Interactions:
  - Accessed by the Recommendation Engine to retrieve candidate restaurant sets.
  - Accessed by user routes for auth, preferences, likes, and friends.
  - Geospatial queries require a `2dsphere` index on the `location` field.
- Source code: [`/api/db/`](api/db/)

## API Gateway / Backend Server

- Technology: FastAPI (Python), Uvicorn
- Responsibilities: Expose REST endpoints for recommendations, user management, and group sessions. Orchestrate requests between the frontend, recommendation engine, and database.
- Interactions:
  - Handles all frontend HTTP requests.
  - Routes requests to recommendation services, user services, and group services.
  - Applies CORS middleware for frontend communication.
- Source code: [`/api/routes`](api/)

## Data & Model Training Pipeline

- Technology: pandas, scikit-learn, Parquet files
- Responsibilities: Preprocess restaurant features and user interaction data, train the Content-Based (TF-IDF) and Collaborative Filtering (item-based CF) models, and export trained `.pkl` files.
- Interactions:
  - Produces offline recommendation models consumed by the Recommendation Engine during runtime.
  - Reads the preprocessed restaurant feature dataset and user interaction dataset stored as Parquet files.
  - Outputs trained models to `/models/` directory.
  - `rests_uploader.py` seeds MongoDB from parquet data.
- Source code: [`/api/ml/train_content_based.py`](api/ml/train_content_based.py), [`/api/ml/train_item_cf.py`](api/ml/train_item_cf.py), [`/data/`](data/)

## Enum & Constants Definitions

- Technology: Python Enum, TypeScript constants
- Responsibilities: Provide shared domain definitions that ensure consistency between backend filtering logic and frontend user interfaces.
- Interactions:
  - Backend uses enums for data validation and mapping user preferences to DB queries.
  - Frontend constants mirror the enum values for onboarding option display.
- Source code: [`/enums/models_enums.py`](enums/models_enums.py), [`/frontend/src/constants/onboardingOptions.ts`](frontend/src/constants/onboardingOptions.ts)

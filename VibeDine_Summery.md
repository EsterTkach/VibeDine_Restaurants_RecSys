# VibeDine -- Project Summary


## Datasets Used
-   **Google Local Reviews Dataset (California)** - Restaurant metadata
-   **Google Local Reviews Dataset (California)** - Restaurant metadata
    including categories, ratings, reviews, opening hours, price level,
    atmosphere, accessibility and offerings.
-   **Google Local Reviews - User Interactions** - Historical user
    ratings used for collaborative filtering.
-   **MongoDB Collections** - Runtime data including registered users,
    onboarding preferences, likes, saved restaurants, viewed restaurants and social connections.


Additional data-related information:
-   The restaurant metadata and interaction datasets were preprocessed
    and cleaned before training.
-   Runtime user interactions are continuously stored in MongoDB and
    complement the offline recommendation models.


-----------------------------------------------------------------------
## Technologies and Frameworks


### Frontend


-   **React**
-   **TypeScript**
-   **Vite**
-   **React Router**
-   **CSS Modules / Custom CSS**


### Backend


-   **FastAPI**
-   **Python**
-   **REST API**
-   **Pydantic**


### Algorithmic


-   **Item-Based Collaborative Filtering**
-   **Content-Based Recommendation**
-   **Cold-Start Recommendation**
-   **Hybrid Recommendation Strategy**


### Data Platforms


-   **MongoDB Atlas** -- Stores users, interactions and application
    state.
-   **Parquet** -- Stores preprocessed datasets and trained model
    inputs.


### AI  ?
 


-----------------------------------------------------------------------


## Main Algorithms


-   **Collaborative Filtering** -- Recommends restaurants based on
    similar users' preferences.
-   **Content-Based Recommendation** -- Finds restaurants similar to a
    selected restaurant using restaurant features.
-   **Cold Start** -- Uses onboarding preferences and popular
    restaurants for new users.
-   **Hybrid Recommendation** -- Combines offline preferences with
    online interactions.


------------------------------------------------------------------------


## System Architecture


The project follows a layered architecture:


1.  **Frontend (React)** -- User interface and navigation.
2.  **Backend (FastAPI)** -- REST API and business logic.
3.  **Recommendation Layer** -- Collaborative filtering, content-based
    recommendation and cold-start handling.
4.  **MongoDB** -- Stores users, onboarding data and interactions.
5.  **Offline Models** -- Trained recommendation models loaded during
    runtime.


Typical flow:


1.  User signs up or logs in.
2.  Preferences are collected during onboarding.
3.  Backend retrieves relevant user information.
4.  Recommendation engine generates personalized suggestions.
5.  Results are returned to the frontend.
6.  Future interactions are saved to improve recommendations.


------------------------------------------------------------------------


## Development Environment


-   React + Vite for frontend development.
-   FastAPI backend running locally with Uvicorn.
-   MongoDB Atlas cloud database.
-   GitHub workflow using feature branches and pull requests.


------------------------------------------------------------------------


## Development Evolution


-   **Milestone 1** -- Authentication and onboarding.
-   **Milestone 2** -- User interactions (likes, saves, views).
-   **Milestone 3** -- Content-Based recommendation engine.
-   **Milestone 4** -- Collaborative Filtering integration.
-   **Milestone 5** -- Candidate filtering and recommendation pipeline.
-   **Milestone 6** -- Friends system and profile endpoints.
-   **Milestone 7** -- Frontend integration and loading workflow.


------------------------------------------------------------------------


## Evaluation


Recommendation quality was evaluated using:


-   Offline recommendation quality metrics.
-   Manual inspection of recommendation relevance.
-   End-to-end testing of frontend/backend integration.
-   Functional testing for authentication, onboarding and recommendation flows.


------------------------------------------------------------------------


## Main Features


-   User registration and authentication.
-   Personalized onboarding questionnaire.
-   Personalized restaurant recommendations.
-   Similar restaurant recommendations.
-   Cold-start support.
-   Restaurant likes, saves and view history.
-   User profile.
-   Friends management.
-   Filtering by cuisine, atmosphere, price and dietary preferences.
-   Responsive frontend interface.


------------------------------------------------------------------------


## Open Issues, Limitations, and Future Work


-   Improve hybrid recommendation weighting.
-   Add real-time recommendation updates.
-   Expand social recommendation features.
-   Improve geographical recommendations.
-   Add model retraining pipeline.
-   Improve recommendation explanations.


------------------------------------------------------------------------


## Additional Comments

-   The home page carusele feature "Popular Near You" is sensetive to user location and urban density. 
        In order to experiance the caruseles feature as intented please make a new user in Los Angeles, California. 








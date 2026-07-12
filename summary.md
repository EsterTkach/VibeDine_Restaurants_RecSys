# Project Summary


## Datasets Used

The recommendation models were trained on two subsets of the **Google Local Data (2021)** dataset. [link to repository](https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/#complete-data).

- **Metadata Dataset** — Restaurant metadata including categories, ratings, reviews, opening hours, price level, accessibility, service options, dining options, and other business attributes. 

- **User Reviews Dataset** — Historical user ratings used to train the Item-Based Collaborative Filtering model.

- **MongoDB Collections**  
  Runtime application data including registered users, onboarding preferences, likes, saved restaurants, viewed restaurants, friendships, and group recommendation sessions.

Additional data-related information:

- The original Google Local Data dataset was preprocessed into a **5-core** subset, ensuring that every user and every restaurant had at least five interactions.
- Restaurant metadata and user interactions were further cleaned and converted into Parquet files before training.
- Runtime user interactions are stored in MongoDB and complement the offline recommendation models.

&nbsp;<br>

## Technologies and Frameworks


### Frontend


- **React** — Builds the single-page application and user interface.
- **TypeScript** — Provides static typing and improves maintainability.
- **Vite** — Development server and frontend build tool.
- **React Router** — Client-side routing and navigation.
- **Tailwind CSS** — Responsive UI styling and layout.


### Backend


- **FastAPI** — REST API implementation and request orchestration.
- **Python** — Backend services and recommendation logic.
- **Pydantic** — Request validation and data serialization.
- **Uvicorn** — ASGI application server.


### Algorithmic

- **scikit-learn** — TF-IDF vectorization and cosine similarity computations.
- **TF-IDF Vectorizer** — Restaurant feature representation.
- **Cosine Similarity** — Similarity computation between restaurants.
- **SciPy Sparse Matrices** — Efficient storage and processing of interaction matrices.
- **NumPy** — Numerical computations throughout the recommendation pipeline.
- **Pandas** — Dataset preprocessing and feature engineering.


### Data Platforms

- **MongoDB Atlas** — Stores runtime users, interactions, onboarding preferences, friendships, and recommendation sessions.
- **Parquet** — Stores preprocessed datasets used for offline model training.

&nbsp;<br>

## Main Algorithms

- **Candidate Retrieval Pipeline** — Retrieves restaurant candidates from MongoDB by filtering restaurants according to selected cuisines, vibes, dietary preferences, accessibility, location, quality thresholds, and other contextual filters. 
This pipeline is used to generate candidate sets for homepage carousels, Vibe Matcher, cold-start recommendations, and group recommendation sessions.

- **Content-Based Filtering (TF-IDF)** — Powers the **Similar Restaurants** feature and contributes personalized scores for the Hybrid Recommendation Engine.

- **Item-Based Collaborative Filtering** — Learns restaurant similarities from historical user interactions and contributes personalized scores for the Hybrid Recommendation Engine.

- **Adaptive Hybrid Recommendation** — Combines Content-Based and Collaborative Filtering scores to generate all personalized recommendations throughout the system, including homepage carousels, Vibe Matcher, and Group Recommendation sessions.

- **Cold-Start Recommendation** — Generates recommendations for new users using onboarding preferences until sufficient interaction history is available.

- **Interactive Group Recommendation** — Powers the **Group Sync** feature by aggregating personalized hybrid recommendations and recomputing them after each round of group feedback.

The recommendation engine combines several complementary algorithms to support different recommendation scenarios.





&nbsp;<br>


## System Architecture

## System Architecture

VibeDine follows a layered architecture that separates the user interface, business logic, recommendation algorithms, and data management.

The React frontend communicates exclusively with the FastAPI backend through REST APIs. The backend orchestrates the recommendation process by retrieving restaurant candidates from MongoDB, invoking the recommendation engine, and returning ranked recommendations to the client. Offline-trained recommendation models are loaded into memory during application startup, while MongoDB stores all runtime user data and interactions.

Typical flow:

1. A user signs in or creates a new account.
2. The frontend sends the user's request and preferences to the FastAPI backend.
3. The backend retrieves restaurant candidates from MongoDB according to the requested filters and user preferences.
4. The recommendation engine computes Content-Based and/or Collaborative Filtering scores, depending on the user's interaction history.
5. The Hybrid Recommendation Engine combines the scores and ranks the recommendations.
6. The ranked recommendations are returned to the frontend and displayed to the user.
7. User likes are stored in MongoDB.
8. Future recommendations immediately incorporate the latest online interactions while continuing to use the offline-trained recommendation models.


## Development Environment

- **Visual Studio Code** — Backend and machine learning development.
- **Github copilot & Claude** — Frontend development and rapid UI iteration.
- **Git & GitHub** — Version control using feature branches and pull requests.
- **Docker** — Containerized deployment of the frontend and backend services.
- **MongoDB Atlas** — Cloud-hosted database.

&nbsp;<br>


## Development Evolution


The project evolved incrementally from a basic recommendation prototype into a complete end-to-end recommendation platform.

- **Milestone 1** — User authentication and onboarding questionnaire.
- **Milestone 2** — User interaction tracking (likes, saves, views).
- **Milestone 3** — Content-Based recommendation engine.
- **Milestone 4** — Item-Based Collaborative Filtering integration.
- **Milestone 5** — Hybrid recommendation engine with adaptive weighting.
- **Milestone 6** — Candidate retrieval pipeline and recommendation filtering.
- **Milestone 7** — Friends system, user profiles, and frontend integration.
- **Milestone 8** — Interactive group recommendation sessions with iterative recommendation updates.

&nbsp;<br>



## Evaluation

Recommendation quality was evaluated using:

- Functional testing of all recommendation workflows.
- Manual validation of recommendation relevance across different user profiles.
- End-to-end integration testing between the frontend and backend.
- API testing using Swagger and Postman.
- Cold-start testing using newly created users.
- Group recommendation testing with users exhibiting different preference profiles.



## Main Features


-   User registration and authentication.
-   Personalized onboarding questionnaire.
-   Personalized restaurant recommendations.
-   Similar restaurant recommendations.
-   Cold-start support.
-   Restaurant likes history.
-   User profile.
-   Friends management.
-   Filtering by cuisine, atmosphere, price and dietary preferences.
-   Responsive frontend interface.
-   Group recommendation sessions.
-   Adaptive hybrid recommendation engine.



## Limitations & Future Work

### Current Limitations

- The recommendation models were trained on restaurant data from **California**, which may limit recommendation quality in other geographic regions.
- Recommendation models need to be retrained periodically to include newly collected interaction data.
- Group recommendations currently require users to share a single device during the recommendation session.

### Future Work

- Expand recommendation coverage beyond California using additional Google Local Data.
- Generate fully personalized homepage carousels.
- Introduce an interactive recommendation map.
- Support multi-device collaborative group recommendation sessions.
- Incorporate online learning from real-time user interactions.
- Integrate restaurant payment platforms (e.g., Tabit).
- Encourage post-visit feedback to continuously improve recommendation quality.
- Incorporate weather-aware recommendations.
- Recommend work-friendly cafés and restaurants for studying and remote work.


&nbsp;<br>


## Additional Comments

One of the main engineering challenges was combining offline-trained recommendation models with continuously evolving online user interactions. The final hybrid architecture allows the system to leverage both historical data and newly collected feedback without requiring model retraining after every interaction.


The **"Popular Near You"** carousel relies on the user's geographic location and local restaurant density.

For the best experience, create a new user located in **Los Angeles, California**, where the dataset provides the richest restaurant coverage.
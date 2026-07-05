
# Project Summary

## Datasets Used

- **Google Local Data (2021)** - Contains business metadata and user reviews collected from Google Maps across the United States. [link to repository](https://mcauleylab.ucsd.edu/public_datasets/gdrive/googlelocal/#complete-data).

Additional data-related information:

For our recommendation system, we used two main components:

- **Metadata dataset** – used for restaurant information and content-based recommendations.
- **Review dataset** – used for collaborative filtering and user interaction modeling.

**Our preprocessing pipeline included:**

- Filtered the original dataset to include only restaurant-related businesses.
- Built a **Source5Core** dataset by retaining only restaurants and users with at least five interactions, creating a denser interaction matrix for collaborative filtering.
- Converted the processed data into structured JSON documents for MongoDB.
- Generated optimized Parquet files for machine learning.
- Constructed the collaborative filtering interaction matrix.
- Extracted restaurant feature tables for the content-based recommendation model.

Dataset Statistics

- 40,645 restaurants
- 9.7 million reviews

&nbsp;<br>

## Technologies and Frameworks

### Frontend
-   **React** — for ...
-   **TypeScript**
-   **Vite**
-   **React Router**
-   **CSS Modules / Custom CSS**

- **Gardio** — for ...
- **NiceGUI** — for ...
- ...

### Backend

- **FastAPI** — for ...
- **Flask** — for ...
- ...

### Algorithmic

- **PyTorch** — for matrix factorization...
- **scikit-learn** — for content-based recommendations...
- ...

### Data Platforms

- **MySQL** — for storing main user interactions...
- **Redis** — for caching models and user interactions...

### AI

- **OpenAI Model X** — for embedding items...
- ...

&nbsp;<br>

## Main Algorithms

A brief summary of the key algorithms and features developed:

- **Collaborative filtering (SVD)** — for feature 1 (searching users …)
- **Collaborative filtering (Item Based)** — for feature 2 (searching relevant items…)
- **Content-based (TF-IDF)** — for feature 3 (relevant categories)
- **Embedding model (OpenAI Model X)** — for feature 4 (help in bootstrapping new items)

&nbsp;<br>

## System Architecture

Describe the high-level architecture of the system, including the main components, how they communicate, and the role of each layer.

Optional system flow:

1. Describe how a user action enters the system.
2. Describe how the system retrieves the relevant data.
3. Describe how the system generates or selects recommendations.
4. Describe how recommendations are returned to the user.
5. Describe how user feedback is stored and used for future improvement.


## Development Environment
- **Cursor** - used for the UI development
- **VSCode + ChatGPT** - used for the algorithmic modules

&nbsp;<br>

## Development Evolution

Describe the main stages of your system development, major changes, and lessons learned.

Example:

- **Milestone 1:** Initial prototype with basic search and static recommendations.
- **Milestone 2:** Added collaborative filtering using PyTorch.
- **Milestone 3:** Integrated OpenAI model for better item embeddings.
- **Milestone 4:** Switched to Redis for faster caching.
- **Milestone 5:** Improved search engine ranking using TF-IDF.

&nbsp;<br>

## Evaluation

Describe how the recommendation quality was evaluated.

## Main Features

Describe the main features of your system.

Please include:

- Core recommendation features.
- Any feature that makes the project unique, creative, or technically interesting.

## Open Issues, Limitations, and Future Work

- Known limitations or challenges.
- Planned improvements.
- Potential next steps.

&nbsp;<br>

## Additional Comments

Any extra insights, difficulties, tricks, or interesting stories you want to share.
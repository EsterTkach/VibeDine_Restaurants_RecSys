import { useNavigate } from "react-router-dom";

import AppShell from "../layouts/AppShell";

import "./RestaurantPage.css";

export default function RestaurantPage() {
  const navigate = useNavigate();

  return (
    <AppShell>
      <div className="restaurant-page">

        <div className="restaurant-hero">

          <img
            src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0"
            alt="Nobu"
          />

        </div>

        <div className="restaurant-content">

          <button
            className="back-btn"
            onClick={() => navigate(-1)}
          >
            ← Back
          </button>

          <h1>Nobu</h1>

          <div className="restaurant-meta">

            <span>⭐ 4.9</span>

            <span>$$$$</span>

            <span>Japanese</span>

          </div>

          <div className="recommendation-tag">
            Recommended For You
          </div>

          <p className="restaurant-description">
            One of the most popular
            Japanese dining experiences
            in the area.
          </p>

          <button className="action-btn">
            ❤️ Like Restaurant
          </button>

          <button className="action-btn secondary">
            👎 Dislike Restaurant
          </button>

          <button className="maps-btn">
            📍 Open In Maps
          </button>

        </div>

      </div>
    </AppShell>
  );
}
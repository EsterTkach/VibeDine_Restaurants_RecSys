import { useState, useEffect } from "react";
import AppShell from "../layouts/AppShell";
import RestaurantCard from "../components/RestaurantCard";
import BottomNav from "../components/BottomNav";
import VibeMatcherModal from "../components/VibeMatcherModal";
import ComingSoonModal from "../components/ComingSoonModal";
import { useNavigate, useLocation } from "react-router-dom";

import { restaurants } from "../data/restaurants";

import "./HomePage.css";


export default function HomePage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [showSearchBanner, setShowSearchBanner] =
  useState(false);
  const location = useLocation();
  const [showVibeModal, setShowVibeModal] = useState(false);
  const [showComingSoon, setShowComingSoon] = useState(false);

  const handleVibeMatchClick = () => {
    setShowVibeModal(true);
  };

  const handleVibeModalClose = () => {
    setShowVibeModal(false);
  };

  const handleVibeMatchSubmit = () => {
    setShowVibeModal(false);
    navigate("/loading", { state: { fromVibeMatcher: true } });
  };

  const handleComingSoonClose = () => {
    setShowComingSoon(false);
  };

  // Show Coming Soon modal when returning from loading page after Vibe Matcher
  useEffect(() => {
    if (location.state?.fromVibeMatcher) {
      setShowComingSoon(true);
      
      // Clear the state so modal doesn't show again on navigation
      window.history.replaceState({}, document.title);
    }
  }, [location]);

  return (
    <AppShell>
      <div className="home-page">

        <div className="home-header">

          <div>
            <h1>
              Good Afternoon, Aya 👋
            </h1>

            <p>
              Find your next favorite spot
            </p>
            <p className="location-tag">
              📍 California • Demo Location
            </p>
          </div>

          <div className="profile-avatar">
            🍽️
          </div>

        </div>

        <div className="search-bar" onClick={handleVibeMatchClick}>
          <span className="search-icon">✨</span>
          <span className="search-text">Vibe Matcher</span>
        </div>
        <div className="hero-card">

        <img
          src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0"
          alt="Nobu"
        />

        <div className="hero-overlay">

          <span className="hero-badge">
            Tonight's Pick
          </span>

          <h2>Nobu</h2>

          <p>
            Japanese • Fine Dining
          </p>

          <button
            className="hero-btn"
            onClick={() =>
              navigate("/restaurant")
            }
          >
            View Restaurant →
          </button>

        </div>

      </div>
        <section>
          <h2>Recommended For You</h2>

          <div className="carousel">
            {restaurants.map((restaurant) => (
              <RestaurantCard
                key={restaurant.id}
                restaurant={restaurant} />
            ))}
          </div>
        </section>

        <section>
          <h2>Popular Near You</h2>

          <div className="carousel">
            {restaurants.map((restaurant) => (
              <RestaurantCard
                key={`popular-${restaurant.id}`}
                restaurant={restaurant} />
            ))}
          </div>
        </section>

        <section>
          <h2>Date Night Picks</h2>

          <div className="carousel">
            {restaurants.map((restaurant) => (
              <RestaurantCard
                key={`date-${restaurant.id}`}
                restaurant={restaurant} />
            ))}
          </div>
        </section>

      </div>

      {/* Vibe Matcher Modal */}
      <VibeMatcherModal
        isOpen={showVibeModal}
        onClose={handleVibeModalClose}
        onSubmit={handleVibeMatchSubmit}
      />

      {/* Coming Soon Modal */}
      <ComingSoonModal
        isOpen={showComingSoon}
        onClose={handleComingSoonClose}
      />

      <BottomNav />
    </AppShell>
  );
}
import { useState, useEffect } from "react";
import AppShell from "../layouts/AppShell";
import RestaurantCard from "../components/RestaurantCard";
import BottomNav from "../components/BottomNav";
import VibeMatcherModal from "../components/VibeMatcherModal";
import ComingSoonModal from "../components/ComingSoonModal";
import { useNavigate, useLocation } from "react-router-dom";
import RestaurantRow from '../components/RestaurantRow';

import { restaurants } from "../data/restaurants";

import "./HomePage.css";

export default function HomePage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [showSearchBanner, setShowSearchBanner] = useState(false);
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
      {/* We kept the up/down scrollbar controls on the main page, 
        but removed the global 'gap' rule so your top elements don't separate.
      */}
      <div 
        className="home-page"
        style={{
          display: 'flex',
          flexDirection: 'column',
          height: 'calc(100vh - 20px)', /* Fills the window height */
          overflowY: 'auto',           /* CRITICAL: Keeps up/down scrolling alive */
          paddingBottom: '120px',      /* Safety cushion at the very bottom */
          boxSizing: 'border-box'
        }}
      >

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
              onClick={() => navigate("/restaurant")}
            >
              View Restaurant →
            </button>
          </div>
        </div>

        {/* NEW: This dedicated container holds only your carousels. 
          It spaces them perfectly apart from each other and sits tightly beneath the hero card.
        */}
        <div 
          className="carousels-container"
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '36px',       /* Perfectly spaces the rows apart from one another */
            marginTop: '0px'  /* Controls the exact distance between the hero card and the first carousel */
          }}
        >
          <RestaurantRow 
            title="Recommended For You" 
            emoji="✨" 
            restaurants={restaurants} 
          />

          <RestaurantRow 
            title="Popular Near You" 
            emoji="🔥" 
            restaurants={restaurants} 
          />

          <RestaurantRow 
            title="Cafe" 
            emoji="☕" 
            restaurants={restaurants} 
          />

          <RestaurantRow 
            title="Sushi" 
            emoji="🍣" 
            restaurants={restaurants} 
          />

          <RestaurantRow 
            title="Italian" 
            emoji="🍝" 
            restaurants={restaurants} 
          />

          <RestaurantRow 
            title="Dessert" 
            emoji="🍰" 
            restaurants={restaurants} 
          />
        </div>

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
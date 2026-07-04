import { useState, useEffect } from "react";
import AppShell from "../layouts/AppShell";
import BottomNav from "../components/BottomNav";
import VibeMatcherModal from "../components/VibeMatcherModal";
import ComingSoonModal from "../components/ComingSoonModal";
import { useNavigate } from "react-router-dom";
import RestaurantRow from '../components/RestaurantRow';
import { getHomeCarousels, getVibeMatchRecommendations } from "../api/restaurants";
import "./HomePage.css";

import { useAuth } from "../contexts/AuthContext";
import { useHome } from "../contexts/HomeContext";
import axios from "axios";

export default function HomePage() {
  const navigate = useNavigate();
  const [showVibeModal, setShowVibeModal] = useState(false);
  const [showComingSoon, setShowComingSoon] = useState(false);

  // LIVE DATA STATES
  
  const { username, setUsername, setUserId } = useAuth();
  const {
    carousels,
    setCarousels,
    hasLoadedHome,
    setHasLoadedHome,
  } = useHome();
  const [loading, setLoading] = useState<boolean>(true);
  const [showAccountMenu, setShowAccountMenu] = useState(false);
  
  // New clean UI error message state tracker
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const trueAvatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(
    username
  )}&background=3d2817&color=fff&bold=true&rounded=true`;

  const getGreeting = (): string => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) return "Good Morning";
    if (hour >= 12 && hour < 17) return "Good Afternoon";
    if (hour >= 17 && hour < 22) return "Good Evening";
    return "Good Night";
  };

  const handleVibeMatchClick = () => {
    setShowVibeModal(true);
  };

  const handleVibeModalClose = () => {
    setShowVibeModal(false);
  };

  const handleVibeMatchSubmit = async (filters: any) => {
  setLoading(true);
  setErrorMessage(null);

  const userId =
    localStorage.getItem("user_id") ||
    localStorage.getItem("userId") ||
    "default_user";

  try {
    const data = await getVibeMatchRecommendations(
      userId,
      filters
    );
    setShowVibeModal(false);
    navigate("/loading", {
      state: {
        nextPage: "/vibe-match",
        recommendations: data.recommendations || [],
        filters,
      },
    });
  } catch (error) {
    console.error("Failed to load vibe matches:", error);
    setErrorMessage("Could not load vibe matches. Please try again.");
  } finally {
    setLoading(false);
  }
};

  const handleComingSoonClose = () => {
    setShowComingSoon(false);
  };

  const handleLogout = () => {
    setUserId("");
    setUsername("");
    setCarousels([]);
    setHasLoadedHome(false);
    setShowAccountMenu(false);
    navigate("/login", { replace: true });
  };
  console.log("HomePage render");
  // BACKEND INTEGRATION EFFECT
  useEffect(() => {
    console.log("Home useEffect started");
    async function fetchDashboardData() {
      if (hasLoadedHome) {
        console.log("Home data already loaded, skipping fetch.");
        setLoading(false);
        return;
      }
      try {
        setLoading(true);
        setErrorMessage(null); // Reset previous errors on reload
        
        const currentUserId = localStorage.getItem("user_id");
        if (!currentUserId) {
          navigate("/login", { replace: true });
          return;
        }
        const data = await getHomeCarousels(currentUserId);

        console.log("Home carousels response:", data);

        setCarousels(data.carousels || []);
        setHasLoadedHome(true);
        console.log("Carousels:", data.carousels);

        }

        catch (error) {
        console.error(error);
        if (axios.isAxiosError(error)) {
          console.log(error.response);
}
      } finally {
        setLoading(false);
      }
    }
    console.log("fetchDashboardData called");
    fetchDashboardData();
  }, []);

  const emojiMap: Record<string, string> = {
    recommended_for_you: "✨",
    popular_near_you: "🔥",
    popular_at_this_hour: "⏰",
    you_might_like: "👍",
    hidden_gems: "💎"
  };

  return (
    <AppShell>
      <div className="home-page">
        <div className="home-header">
          <div>
            <h1>
              {getGreeting()}, {username}!👋
            </h1>
            <p>Find your next favorite spot</p>
          </div>

          <div className="profile-avatar-container">
            <button
              className="profile-avatar-button"
              onClick={() => setShowAccountMenu((value) => !value)}
              aria-label="Open account menu"
            >
              {loading && !errorMessage ? (
                <div className="profile-avatar-loader">⏳</div>
              ) : (
                <img 
                  src={trueAvatarUrl} 
                  alt={`${username}'s Profile Avatar`} 
                  className="profile-avatar"
                  style={{ width: "44px", height: "44px", borderRadius: "50%", objectFit: "cover" }}
                />
              )}
            </button>

            {showAccountMenu && (
              <div className="account-menu">
                <button className="account-menu-button" onClick={handleLogout}>
                  Log out
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="search-bar" onClick={handleVibeMatchClick}>
          <span className="search-icon">🪄</span>
          <span className="search-text">Vibe Matcher</span>
        </div>

        <div 
          className="search-bar" 
          onClick={() => navigate("/group")}
          style={{ marginTop: "-10px" }}
        >
          <span className="search-icon">👥</span>
          <span className="search-text">Plan With Friends</span>
        </div>

        <div 
          className="carousels-container"
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '36px',
            marginTop: '24px'
          }}
        >
          {loading ? (
            <div className="text-center p-10 text-gray-400">Loading your customized feed...</div>
          ) : errorMessage ? (
            // CLEAN ALTERNATIVE: Replaces carousels with an interactive alert box if something breaks
            <div className="error-banner" style={{ textAlign: 'center', padding: '40px 20px', background: '#fff5f5', borderRadius: '12px', border: '1px dashed #feb2b2', color: '#c53030' }}>
              <span style={{ fontSize: '32px' }}>⚠️</span>
              <h3 style={{ margin: '12px 0 6px', fontWeight: 'bold' }}>Feed Temporarily Unavailable</h3>
              <p style={{ fontSize: '14px', opacity: 0.8, maxWidth: '400px', margin: '0 auto' }}>{errorMessage}</p>
            </div>
          ) : (
            carousels.map((carousel) => (
              <RestaurantRow 
                key={carousel.id}
                title={carousel.title} 
                emoji={emojiMap[carousel.id] || "📍"} 
                restaurants={carousel.items} 
              />
            ))
          )}
        </div>
      </div>

      <VibeMatcherModal
        isOpen={showVibeModal}
        onClose={handleVibeModalClose}
        onSubmit={handleVibeMatchSubmit}
      />

      <ComingSoonModal
        isOpen={showComingSoon}
        onClose={handleComingSoonClose}
      />

      <BottomNav />
    </AppShell>
  );
}
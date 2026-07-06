import axios from "axios";
import { useState, useEffect } from "react";
import AppShell from "../layouts/AppShell";
import BottomNav from "../components/BottomNav";
import VibeMatcherModal from "../components/VibeMatcherModal";
import ComingSoonModal from "../components/ComingSoonModal";
import { useNavigate } from "react-router-dom";
import RestaurantRow from '../components/RestaurantRow';
import { getHomeCarousels, getVibeMatchRecommendations } from "../api/restaurants";
import "./HomePage.css";

import { defaultUserData, useAuth } from "../contexts/AuthContext";
import { useHome } from "../contexts/HomeContext";
import FoodAvatar from "../components/FoodAvatar";
import PersonalizationProgressPill from "../components/PersonalizationProgressPill";
import CarouselsLoader from "../components/CarouselsLoader";



export default function HomePage() {
  const navigate = useNavigate();
  const [showVibeModal, setShowVibeModal] = useState(false);
  const [showComingSoon, setShowComingSoon] = useState(false);

  // LIVE DATA STATES

  const { userData, setUserData } = useAuth();
  const userId = userData.user_id;

   const trueAvatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(
    userData.name
  )}&background=3d2817&color=fff&bold=true&rounded=true`;

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

  if (!userId) {
    navigate("/login", { replace: true });
    return;
  }

  try {
    const data = await getVibeMatchRecommendations(userId, filters);

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
    setUserData(defaultUserData);
    localStorage.removeItem("user_data");

    setCarousels([]);
    setHasLoadedHome(false);
    setShowAccountMenu(false);
    navigate("/login", { replace: true });
  };
  console.log("HomePage render");
  // BACKEND INTEGRATION EFFECT
  // Fires only on mount and when the logged-in user changes. Mid-session
  // likes set `hasLoadedHome=false` silently (see HomeContext); we pick that
  // up on the next HomePage mount (i.e., when the user navigates back).
  // eslint-disable-next-line react-hooks/exhaustive-deps
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

        if (!userId) {
          navigate("/login", { replace: true });
          return;
        }
        const data = await getHomeCarousels(userId);

        console.log("Home carousels response:", data);

        setCarousels(data.carousels || []);
        setHasLoadedHome(true);
        console.log("Carousels:", data.carousels);
        }

        catch (error) {
        console.error(error);
        if (axios.isAxiosError(error)) {
          console.log(error.response);
          setErrorMessage("We couldn't connect to the server. Please check your network and try again.");
}
      } finally {
        setLoading(false);
      }
    }
    console.log("fetchDashboardData called");
    fetchDashboardData();
  }, [userId]);

  const emojiMap: Record<string, string> = {
    recommended_for_you: "✨",
    popular_near_you: "🔥",
    popular_at_this_hour: "⏰",
    you_might_like: "👍",
    hidden_gems: "💎",
  };

  return (
    <AppShell>
      <div className="home-page">
        <div className="home-header">
          <div className="home-text">
            <h1 className="greeting">
              <span>{getGreeting()},</span>
              <span>{userData.name}! 👋</span>
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
                <FoodAvatar avatar_index={userData.avatar_index} size={90} />
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
          <span className="search-text">Vibe Matcher</span>{" "}
          <span className="search-icon">🪄</span>
        </div>

        <div
          className="search-bar"
          onClick={() => navigate("/group")}
          style={{ marginTop: "-10px" }}
        >
          <span className="search-text">Plan With Friends</span>{" "}
          <span className="search-icon">👥</span>
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
          {loading && carousels.length === 0 ? (
            <CarouselsLoader />
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
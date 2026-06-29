import { useState, useEffect } from "react";
import AppShell from "../layouts/AppShell";
import BottomNav from "../components/BottomNav";
import VibeMatcherModal from "../components/VibeMatcherModal";
import ComingSoonModal from "../components/ComingSoonModal";
import { useNavigate, useLocation } from "react-router-dom";
import RestaurantRow from '../components/RestaurantRow';
import type { CarouselData } from '../types';

import { userService } from "../api/services";
import "./HomePage.css";

export default function HomePage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [showVibeModal, setShowVibeModal] = useState(false);
  const [showComingSoon, setShowComingSoon] = useState(false);

  // LIVE DATA STATES
  const [username, setUsername] = useState<string>(
    localStorage.getItem("username") || location.state?.username || "User"
  );
  const [carousels, setCarousels] = useState<CarouselData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  
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

  const handleVibeMatchSubmit = () => {
    setShowVibeModal(false);
    navigate("/loading", { state: { fromVibeMatcher: true } });
  };

  const handleComingSoonClose = () => {
    setShowComingSoon(false);
  };

  // BACKEND INTEGRATION EFFECT
  useEffect(() => {
    async function fetchDashboardData() {
      try {
        setLoading(true);
        setErrorMessage(null); // Reset previous errors on reload
        
        const currentUserId = localStorage.getItem("user_id") || "default_user";

        const [carouselRes, profileData] = await Promise.all([
          fetch(`/home-carousels?user_id=${currentUserId}&top_k=25`),
          userService.getProfile().catch(() => ({ name: username }))
        ]);

        if (carouselRes.ok) {
          const data = await carouselRes.json();
          setCarousels(data.carousels || []);
        } else {
          // Captures 404s or 500s directly from server response
          setErrorMessage(`Failed to load feed rows (${carouselRes.status}). Please check server routing configuration.`);
        }

        if (profileData && profileData.name) {
          setUsername(profileData.name);
          localStorage.setItem("username", profileData.name);
        }

      } catch (error) {
        console.error("Layout API network connection failure:", error);
        setErrorMessage("Unable to connect to the recommendations server. Please verify your backend is running.");
      } finally {
        setLoading(false);
      }
    }

    fetchDashboardData();
  }, []);

  useEffect(() => {
    if (location.state?.fromVibeMatcher) {
      setShowComingSoon(true);
      window.history.replaceState({}, document.title);
    }
  }, [location]);

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
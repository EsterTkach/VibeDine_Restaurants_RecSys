import { useState, useEffect, useMemo } from "react";
import AppShell from "../layouts/AppShell";
import BottomNav from "../components/BottomNav";
import VibeMatcherModal from "../components/VibeMatcherModal";
import ComingSoonModal from "../components/ComingSoonModal";
import { useNavigate, useLocation } from "react-router-dom";
import RestaurantRow from '../components/RestaurantRow';
import type { Restaurant } from '../types';

// CHANGED: Routing through our centralized services module
import { restaurantService, userService } from "../api/services";

// Keeping your static data import as an absolute fallback
import { restaurants as mockRestaurants } from "../data/restaurants";

import "./HomePage.css";

export default function HomePage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [showVibeModal, setShowVibeModal] = useState(false);
  const [showComingSoon, setShowComingSoon] = useState(false);

  // LIVE DATA STATES
  const [username, setUsername] = useState<string>(
    localStorage.getItem("username") || location.state?.username || "Mock User"
  );
  const [liveRestaurants, setLiveRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // CHANGED: True dynamic avatar URI matching active username state variables
  const trueAvatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(
    username
  )}&background=3d2817&color=fff&bold=true&rounded=true`;

  // Helper logic to compute the current system greeting message
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

  // 1. BACKEND INTEGRATION EFFECT
useEffect(() => {
  async function fetchDashboardData() {
    try {
      setLoading(true);
      
      const [restaurantData, profileData] = await Promise.all([
        restaurantService.getAll(),
        userService.getProfile().catch(() => ({ name: username }))
      ]);

      if (restaurantData && restaurantData.length > 0) {
        // FIX: Safely transform ApiRecommendation[] into full UI-ready Restaurant[]
        const formattedRestaurants: Restaurant[] = restaurantData.map((item: any) => ({
          gmap_id: item.gmap_id,
          name: item.name,
          avg_rating: item.avg_rating ?? 4.0, // Fallback if missing
          review_count: item.review_count ?? 0, // Fallback if missing
          
          // Provide structural fallbacks for fields the ML backend doesn't output
          category: item.category ?? "Trending Spot", 
          image_url: item.image_url ?? "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=500&auto=format&fit=crop&q=60", 
          price_level: item.price_level ?? "$$",
          is_open: item.is_open ?? true,
        }));

        setLiveRestaurants(formattedRestaurants); // Now matches type constraints perfectly!
      }

      if (profileData && profileData.name) {
        setUsername(profileData.name);
        localStorage.setItem("username", profileData.name);
      }

    } catch (error) {
      console.warn("Backend API offline or loading error. Using stable fallbacks...", error);
      setLiveRestaurants([]);
    } finally {
      setLoading(false);
    }
  }

  fetchDashboardData();
}, []);

  // 2. Vibe Matcher Navigation State Clearance Effect
  useEffect(() => {
    if (location.state?.fromVibeMatcher) {
      setShowComingSoon(true);
      window.history.replaceState({}, document.title);
    }
  }, [location]);

  // Determine what dataset to feed the rows
  const displayRestaurants = useMemo(() => {
    if (liveRestaurants.length > 0) {
      return liveRestaurants;
    }
    
    // If backend is down/loading, map the items and explicitly append the [Mock] flag
    return mockRestaurants.map(res => ({
      ...res,
      name: `[Mock] ${res.name}`
    }));
  }, [liveRestaurants]);

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

          {/* CHANGED: Swapped static character placeholder with full true user dynamic avatar image tag */}
          <div className="profile-avatar-container">
            {loading ? (
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
          <span className="search-icon">✨</span>
          <span className="search-text">Vibe Matcher</span>
        </div>

        <div 
          className="carousels-container"
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '36px',
            marginTop: '10px'
          }}
        >
          <RestaurantRow 
            title="Recommended For You" 
            emoji="✨" 
            restaurants={displayRestaurants} 
          />

          <RestaurantRow 
            title="Popular Near You" 
            emoji="🔥" 
            restaurants={displayRestaurants} 
          />

          <RestaurantRow 
            title="Popular at this hour" 
            emoji="⏰" 
            restaurants={displayRestaurants} 
          />

          <RestaurantRow 
            title="You might like" 
            emoji="👍" 
            restaurants={displayRestaurants} 
          />

          <RestaurantRow 
            title="Hidden gems" 
            emoji="💎" 
            restaurants={displayRestaurants} 
          />
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
import { useState, useEffect, useMemo} from "react";
import AppShell from "../layouts/AppShell";
import BottomNav from "../components/BottomNav";
import VibeMatcherModal from "../components/VibeMatcherModal";
import ComingSoonModal from "../components/ComingSoonModal";
import { useNavigate, useLocation } from "react-router-dom";
import RestaurantRow from '../components/RestaurantRow';
import { restaurantService, userService } from "../api/services";

// Keeping your static data import as an absolute fallback
import { restaurants as mockRestaurants } from "../data/restaurants";

import "./HomePage.css";

interface Restaurant {
  id: string;
  name: string;
  cuisine: string;
  rating: number;
  price: string;
  image: string;
}

export default function HomePage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [search, setSearch] = useState("");
  const [showSearchBanner, setShowSearchBanner] = useState(false);
  const [showVibeModal, setShowVibeModal] = useState(false);
  const [showComingSoon, setShowComingSoon] = useState(false);

  // LIVE DATA STATES
  const [username, setUsername] = useState<string>(location.state?.username || "Mock User");
  const [liveRestaurants, setLiveRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

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
  const BASE_URL = "http://localhost:5000/api";

  async function fetchDashboardData() {
    try {
      setLoading(true);
      
      const [resResponse, userResponse] = await Promise.all([
        fetch(`${BASE_URL}/restaurants`),
        fetch(`${BASE_URL}/user/profile`)
      ]);

      // CHANGED: Only save to state if the server actually returned a 200 OK success
      if (resResponse.ok) {
        const restaurantData = await resResponse.json();
        setLiveRestaurants(restaurantData);
      } else {
        console.warn(`Restaurants endpoint returned status: ${resResponse.status}`);
        setLiveRestaurants([]); // Keep it empty so useMemo handles the Mock tags
      }

      if (userResponse.ok) {
        const userData = await userResponse.json();
        if (userData.name) setUsername(userData.name);
      } else {
        console.warn(`User profile endpoint returned status: ${userResponse.status}`);
        setUsername("Mock User"); // Force stability string on 404
      }

    } catch (error) {
      console.error("Backend completely offline.", error);
      setLiveRestaurants([]);
      setUsername("Mock User");
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
              {getGreeting()}, {username}! 👋
            </h1>
            <p>
              Find your next favorite spot
            </p>
            <p className="location-tag">
              📍 California • Demo Location
            </p>
          </div>

          <div className="profile-avatar">
            {loading ? "⏳" : "🍽️"}
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
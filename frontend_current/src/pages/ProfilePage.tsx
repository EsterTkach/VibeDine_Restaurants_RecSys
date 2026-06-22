import { useNavigate } from "react-router-dom";

import AppShell from "../layouts/AppShell";
import BottomNav from "../components/BottomNav";

import "./ProfilePage.css";

export default function ProfilePage() {
  const navigate = useNavigate();

  // Mock data for liked restaurants
  const likedRestaurants = [
    { id: 1, name: "McDonald's", emoji: "🍔" },
    { id: 2, name: "Sushi Palace", emoji: "🍱" },
    { id: 3, name: "Pasta Perfetto", emoji: "🍝" },
  ];

  // Mock data for disliked restaurants
  const dislikedRestaurants = [
    { id: 1, name: "Burgeranch", emoji: "🍔" },
    { id: 2, name: "Mystery Eats", emoji: "❓" },
  ];

  return (
    <AppShell>

      <div className="profile-page">

        <div className="profile-header">

          <div className="profile-avatar-big">
            A
          </div>

          <h1>Aya Rotbart</h1>

          <p>Food Enthusiast 🍣</p>

        </div>

        <div className="profile-section">

          <h2>Favorite Cuisines</h2>

          <div className="chips">
            <span>🍣 Sushi</span>
            <span>🍷 Italian</span>
            <span>🥐 Brunch</span>
          </div>

        </div>

        {/* Restaurants You Love Section */}
        <div className="profile-section">
          <h2>❤️ Restaurants You Love</h2>
          <div className="restaurant-cards-grid">
            {likedRestaurants.map((restaurant) => (
              <div key={restaurant.id} className="restaurant-favorite-card liked">
                <div className="card-emoji">{restaurant.emoji}</div>
                <div className="card-name">{restaurant.name}</div>
                <div className="card-badge">Loved</div>
              </div>
            ))}
          </div>
        </div>

        {/* Restaurants You Disliked Section */}
        <div className="profile-section">
          <h2>👎 Restaurants You Disliked</h2>
          <div className="restaurant-cards-grid">
            {dislikedRestaurants.map((restaurant) => (
              <div key={restaurant.id} className="restaurant-favorite-card disliked">
                <div className="card-emoji">{restaurant.emoji}</div>
                <div className="card-name">{restaurant.name}</div>
                <div className="card-badge">Disliked</div>
              </div>
            ))}
          </div>
        </div>

        <button
          className="group-btn"
          onClick={() =>
            navigate("/group")
          }
        >
          ✨ Plan With Friends
        </button>

      </div>

      <BottomNav />

    </AppShell>
  );
}
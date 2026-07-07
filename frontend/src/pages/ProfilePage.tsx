import "./ProfilePage.css";
import { useState } from "react";
import { Heart } from "lucide-react";
import { useNavigate } from "react-router-dom";

import AppShell from "../layouts/AppShell";
import BottomNav from "../components/BottomNav";
import { useAuth } from "../contexts/AuthContext";
import { useHome } from "../contexts/HomeContext";
import { useLiked } from "../contexts/LikedContext";
import SectionDivider from "../components/SectionDivider";
import FoodAvatar from "../components/FoodAvatar";
import { DEFAULT_RESTAURANT_IMAGE } from "../constants/imgs";

export default function ProfilePage() {
  const navigate = useNavigate();

  const { userData } = useAuth();
  const { setHasLoadedHome } = useHome();
  const { likedRestaurants, offlineLikedRestaurants, loading, unlikeRestaurant } = useLiked();

  const [removingRestaurantIds, setRemovingRestaurantIds] = useState<string[]>(
    [],
  );

  const handleUnlike = async (restaurantId: string) => {
    setRemovingRestaurantIds((prev) => [...prev, restaurantId]);

    // await userService.unlikeRestaurant(userData.user_id, restaurantId);

    setTimeout(async () => {
      try {

        await unlikeRestaurant(restaurantId);
        setHasLoadedHome(false);
      } catch (err) {
        console.error(err);
      } finally {
        setRemovingRestaurantIds((prev) =>
          prev.filter((id) => id !== restaurantId),
        );
      }
    }, 300);
  };

  return (
    <AppShell>
      <div className="profile-page">
        <div className="profile-header">
          <div className="profile-avatar-big">
            {/* {loading ? "⏳" : avatarLetter} */}
            <FoodAvatar avatar_index={userData.avatar_index} size={110} />
          </div>
          <h1 className="profile-name">{userData.name}</h1>
          <p className="profile-subtitle">Food Explorer 🍜</p>{" "}
        </div>

        {/* Restaurants You Love Section */}
        <div className="profile-section">
          <SectionDivider text="Restaurants You Love" />
          {/* <Heart size={18} fill="#ef4444" color="#ef4444" /> */}
          {loading ? null : likedRestaurants.length === 0 ? (
            <div className="compact-empty-state">
              <span>🍽️</span>

              <h3>No favorite restaurants yet</h3>

              <div className="empty-message">
                <p>Start exploring and tap the ❤️</p>
                <p>to save places you love!</p>
              </div>
            </div>
          ) : (
            <div className="restaurant-cards-grid">
              {likedRestaurants.map((restaurant) => {
                const removing = removingRestaurantIds.includes(
                  restaurant.gmap_id,
                );
                return (
                  <div
                    key={restaurant.gmap_id}
                    className={`restaurant-favorite-card ${
                      removing ? "removing" : ""
                    }`}
                  >
                    <button
                      className="favorite-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleUnlike(restaurant.gmap_id);
                      }}
                    >
                      <Heart
                        size={22}
                        color={removing ? "#9ca3af" : "#ef4444"}
                        fill={removing ? "none" : "#ef4444"}
                      />{" "}
                    </button>
                    <div
                      className="card-image"
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/restaurant/${restaurant.gmap_id}`);
                      }}
                    >
                      <img
                        src={restaurant.image_url || DEFAULT_RESTAURANT_IMAGE}
                        alt=""
                        onError={(e) => {
                          e.currentTarget.src = DEFAULT_RESTAURANT_IMAGE;
                        }}
                      />
                    </div>
                    <div className="card-name">{restaurant.name}</div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Restaurants You Liked Before Section */}
        <div className="profile-section">
          <SectionDivider text="Restaurants You Liked Before" />

          {offlineLikedRestaurants.length === 0 ? (
            <div className="compact-empty-state">
              <span>🕘</span>
              <p>No previous liked restaurants yet</p>
            </div>
          ) : (
            <div className="restaurant-cards-grid">
              {offlineLikedRestaurants.map((restaurant) => (
                <div
                  key={restaurant.gmap_id}
                  className="restaurant-favorite-card"
                >
                  <div
                    className="card-image"
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/restaurant/${restaurant.gmap_id}`);
                    }}
                  >
                    <img
                      src={restaurant.image_url || DEFAULT_RESTAURANT_IMAGE}
                      alt=""
                      onError={(e) => {
                        e.currentTarget.src = DEFAULT_RESTAURANT_IMAGE;
                      }}
                    />
                  </div>
                  <div className="card-name">{restaurant.name}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        <SectionDivider />
      </div>

      <BottomNav />
    </AppShell>
  );
}
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Heart } from "lucide-react";

import AppShell from "../layouts/AppShell";
import BottomNav from "../components/BottomNav";
import { userService } from "../api/services";
import { useAuth } from "../contexts/AuthContext";

import "./ProfilePage.css";
import SectionDivider from "../components/SectionDivider";
import FoodAvatar from "../components/FoodAvatar";

export default function ProfilePage() {
  const navigate = useNavigate();
  const { username, userId } = useAuth();

  // LIVE USER STATE (Defaults to "Mock User" for stability tracking)
  const [profileName, setProfileName] = useState<string>(
    username || "Mock User",
  );
  const [loading, setLoading] = useState<boolean>(true);

  type Restaurant = {
    gmap_id: string;
    name: string;
    image_url: string;
  };

  const [likedRestaurants, setLikedRestaurants] = useState<Restaurant[]>([]);
  const [removingRestaurantIds, setRemovingRestaurantIds] = useState<string[]>(
    [],
  );

  useEffect(() => {
    async function fetchLikedRestaurants() {
      try {
        const userId = "112238780620382660297"; // זמני hardcoded לבדיקה  TODO

        const data = await userService.getLikedRestaurants(userId);
        setLikedRestaurants(data.liked_restaurants);
        console.log("data.liked_restaurants :", data.liked_restaurants);
      } catch (error) {
        console.error("Failed to fetch liked restaurants", error);
      }
    }

    fetchLikedRestaurants();
  }, []);

  useEffect(() => {
    if (username) {
      setProfileName(username);
    }
  }, [username]);

  // Fetch Profile Data on mount
  useEffect(() => {
    setProfileName(username || "User");
  }, [username]);

  const handleUnlike = async (restaurantId: string) => {
    setRemovingRestaurantIds((prev) => [...prev, restaurantId]);

    try {

      await userService.unlikeRestaurant(userId, restaurantId);

      setTimeout(() => {
        setLikedRestaurants((prev) =>
          prev.filter((r) => r.gmap_id !== restaurantId),
        );

        setRemovingRestaurantIds((prev) =>
          prev.filter((id) => id !== restaurantId),
        );
      }, 300);
    } catch (err) {
      console.error(err);
    }
  };

  console.log("profileName :", profileName);

  return (
    <AppShell>
      <div className="profile-page">
        <div className="profile-header">
          <div className="profile-avatar-big">
            {/* {loading ? "⏳" : avatarLetter} */}
            <FoodAvatar userId={username} size={110} />
          </div>
          <h1 className="profile-name">{profileName}</h1>
          <p className="profile-subtitle">Food Explorer</p>{" "}
        </div>

        {/* Restaurants You Love Section */}
        <div className="profile-section">
          <SectionDivider text="Restaurants You Love" />
          {/* <Heart size={18} fill="#ef4444" color="#ef4444" /> */}{" "}
          {likedRestaurants.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🍽️</div>

              <h3>No favorite restaurants yet</h3>

              <p>
                Start exploring and tap the ❤️
                <br />
                to save places you love!
              </p>
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
                      onClick={() => handleUnlike(restaurant.gmap_id)}
                    >
                      <Heart
                        size={22}
                        color={removing ? "#9ca3af" : "#ef4444"}
                        fill={removing ? "none" : "#ef4444"}
                      />{" "}
                    </button>
                    <div className="card-image">
                      <img src={restaurant.image_url} alt={restaurant.name} />
                    </div>
                    <div className="card-name">{restaurant.name}</div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <SectionDivider />
      </div>

      <BottomNav />
    </AppShell>
  );
}
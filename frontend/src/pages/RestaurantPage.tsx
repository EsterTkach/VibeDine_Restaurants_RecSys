import "./RestaurantPage.css";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import apiClient from "../api/client";
import { useAuth } from "../contexts/AuthContext";
import { useLiked } from "../contexts/LikedContext";
import { DEFAULT_RESTAURANT_IMAGE } from "../constants/imgs";


export default function RestaurantPage() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { userData } = useAuth();
  const { likedRestaurants, likeRestaurant, unlikeRestaurant, offlineLikedRestaurants } = useLiked();

  const liked = likedRestaurants.some((r) => r.gmap_id === id);
  const offlineLiked = offlineLikedRestaurants.some((r) => r.gmap_id === id);

  const isLiked = liked || offlineLiked;

  const [restaurant, setRestaurant] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [likeLoading, setLikeLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    apiClient
      .get(`/restaurants/${id}`)
      .then((res) => setRestaurant(res.data))
      .catch(() => setRestaurant(null))
      .finally(() => setLoading(false));
  }, [id]);

  const handleLikeToggle = async () => {
    if (!userData.user_id || !id || likeLoading || offlineLiked) return;

    setLikeLoading(true);

    try {
      if (liked) {
        await unlikeRestaurant(id);
      } else {
        await likeRestaurant(id);
      }
    } catch (error) {
      console.error("Failed to update liked restaurant", error);
    } finally {
      setLikeLoading(false);
    }
  };

  const getCuisineDisplay = () => {
    if (!restaurant?.cuisines?.length) return null;
    return restaurant.cuisines.slice(0, 2).join(" · ");
  };

  const getTodayHours = () => {
    if (!restaurant?.hours) return null;
    const days = [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
    ];
    const today = days[new Date().getDay()];
    return restaurant.hours[today] || null;
  };

  return (
    <AppShell>
      <div className="restaurant-page">
        {loading ? (
          <div className="loading-state">Loading delicious details...</div>
        ) : !restaurant ? (
          <div className="error-state">Restaurant not found.</div>
        ) : (
          <>
            <div className="restaurant-hero">
              <button
                className="back-btn floating-back"
                onClick={() => navigate(-1)}
              >
                ← Back
              </button>

              <img
                src={restaurant.image_url || DEFAULT_RESTAURANT_IMAGE}
                alt=""
                onError={(e) => {
                  e.currentTarget.src = DEFAULT_RESTAURANT_IMAGE;
                }}
                className="hero-img"
              />
            </div>

            <div className="restaurant-content">
              <h1>{restaurant.name}</h1>

              <div className="restaurant-meta">
                {restaurant.avg_rating && (
                  <span>⭐ {restaurant.avg_rating}</span>
                )}
                {restaurant.num_of_reviews && (
                  <span>
                    • {restaurant.num_of_reviews.toLocaleString()} reviews
                  </span>
                )}
                {restaurant.price && <span>• {restaurant.price}</span>}
                {getCuisineDisplay() && <span>• {getCuisineDisplay()}</span>}
              </div>

              {getTodayHours() && (
                <div className="restaurant-hours">
                  🕐 Today: {getTodayHours()}
                </div>
              )}

              {restaurant.address && (
                <div className="restaurant-address">
                  📍 {restaurant.address}
                </div>
              )}

              <div className="actions-row">
                <button
                  className={`action-btn${isLiked ? " liked" : ""}`}
                  onClick={handleLikeToggle}
                  disabled={likeLoading || offlineLiked}
                >
                  {isLiked ? "❤️ Liked" : "🤍 Like"}
                </button>
              </div>

              <button
                className="maps-btn"
                onClick={() =>
                  window.open(
                    `https://maps.google.com/?q=${encodeURIComponent(
                      restaurant.name +
                        (restaurant.address ? ` ${restaurant.address}` : ""),
                    )}`,
                  )
                }
              >
                📍 Open In Maps
              </button>
            </div>
          </>
        )}
      </div>
    </AppShell>
  );
}

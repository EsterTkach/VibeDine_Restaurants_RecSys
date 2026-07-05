import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import apiClient from "../api/client";
import { likeRestaurant, unlikeRestaurant } from "../api/restaurants";
import { useAuth } from "../contexts/AuthContext";
import { useHome } from "../contexts/HomeContext";
import "./RestaurantPage.css";

export default function RestaurantPage() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { userId } = useAuth();
  const { notifyLikeChanged } = useHome();

  const [restaurant, setRestaurant] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [liked, setLiked] = useState(false);
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
    if (!userId || !id || likeLoading) return;
    setLikeLoading(true);
    try {
      if (liked) {
        await unlikeRestaurant(userId, id);
        setLiked(false);
      } else {
        await likeRestaurant(userId, id);
        setLiked(true);
      }
      notifyLikeChanged();
    } catch {
      // silent
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
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
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
              <button className="back-btn floating-back" onClick={() => navigate(-1)}>
                ← Back
              </button>
              {restaurant.image_url && (
                <img src={restaurant.image_url} alt={restaurant.name} className="hero-img" />
              )}
            </div>

            <div className="restaurant-content">
              <h1>{restaurant.name}</h1>

              <div className="restaurant-meta">
                {restaurant.avg_rating && <span>⭐ {restaurant.avg_rating}</span>}
                {restaurant.num_of_reviews && (
                  <span>• {restaurant.num_of_reviews.toLocaleString()} reviews</span>
                )}
                {restaurant.price && <span>• {restaurant.price}</span>}
                {getCuisineDisplay() && <span>• {getCuisineDisplay()}</span>}
              </div>

              {getTodayHours() && (
                <div className="restaurant-hours">🕐 Today: {getTodayHours()}</div>
              )}

              {restaurant.address && (
                <div className="restaurant-address">📍 {restaurant.address}</div>
              )}

              <div className="actions-row">
                <button
                  className={`action-btn${liked ? " liked" : ""}`}
                  onClick={handleLikeToggle}
                  disabled={likeLoading}
                >
                  {liked ? "❤️ Liked" : "🤍 Like"}
                </button>
              </div>

              <button
                className="maps-btn"
                onClick={() =>
                  window.open(
                    `https://maps.google.com/?q=${encodeURIComponent(
                      restaurant.name + (restaurant.address ? ` ${restaurant.address}` : "")
                    )}`
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

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import type { Restaurant } from "../types";

interface Props {
  restaurant: Restaurant;
  variant?: "card" | "list";
}

export default function RestaurantCard({
  restaurant,
  variant = "card",
}: Props) {
  const navigate = useNavigate();
  const [imageLoaded, setImageLoaded] = useState(false);

  const rating = Number(restaurant.avg_rating || 0);
  const reviewCount = restaurant.num_of_reviews;

  return (
    <div
      className={`restaurant-card-home ${variant === "list" ? "restaurant-card-list" : ""}`}
      onClick={() => navigate(`/restaurant/${restaurant.gmap_id}`)}
      style={{ cursor: "pointer" }}
    >
      <div className="restaurant-card-img-wrapper">
        {!imageLoaded && <div className="restaurant-card-img-skeleton" />}
        <img
          src={restaurant.image_url}
          alt={restaurant.name}
          onLoad={() => setImageLoaded(true)}
          onError={(e) => {
            (e.target as HTMLImageElement).src = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&q=80";
            setImageLoaded(true);
          }}
          style={{ opacity: imageLoaded ? 1 : 0 }}
        />
        {restaurant.price && (
          <span className="card-price-overlay">{restaurant.price}</span>
        )}
      </div>

      <div className="restaurant-card-content">
        <h3>{restaurant.name}</h3>

        <div className="restaurant-card-meta">
          <span className="rating-badge">
            ★ {rating.toFixed(1)}
          </span>
          {reviewCount != null && reviewCount > 0 && (
            <span className="review-count">({reviewCount.toLocaleString()})</span>
          )}
        </div>

        {restaurant.cuisine && (
          <p className="cuisine-label">{restaurant.cuisine}</p>
        )}
      </div>
    </div>
  );
}
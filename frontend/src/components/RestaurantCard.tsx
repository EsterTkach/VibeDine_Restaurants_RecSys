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
          style={{ opacity: imageLoaded ? 1 : 0 }}
        />
      </div>

      <div className="restaurant-card-content">
        <h3>{restaurant.name}</h3>

        <div className="restaurant-card-meta">
          <span className="rating-badge">
            ⭐ {Number(restaurant.avg_rating || 0).toFixed(1)}
          </span>
          {restaurant.price && <span className="price-badge">{restaurant.price}</span>}
        </div>

        {restaurant.cuisine && (
          <p className="cuisine-label">{restaurant.cuisine}</p>
        )}
      </div>
    </div>
  );
}
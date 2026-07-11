import { useNavigate } from "react-router-dom";
import type { Restaurant } from "../types";
import { DEFAULT_RESTAURANT_IMAGE } from "../constants/imgs";

interface Props {
  restaurant: Restaurant;
  variant?: "card" | "list";
}

export default function RestaurantCard({
  restaurant,
  variant = "card",
}: Props) {
  const navigate = useNavigate();

  return (
    <div className={`restaurant-card-home ${variant === "list" ? "restaurant-card-list" : ""}`}>
      <img
        src={restaurant.image_url || DEFAULT_RESTAURANT_IMAGE}
        alt=""
        onError={(e) => {
          e.currentTarget.src = DEFAULT_RESTAURANT_IMAGE;
        }}
        onClick={() => navigate(`/restaurant/${restaurant.gmap_id}`)}
        style={{ cursor: "pointer" }}
      />

      <div className="restaurant-card-content">
        <h3>{restaurant.name}</h3>

        <span>
          ⭐ {Number(restaurant.avg_rating || 0).toFixed(1)}
          </span>

        <p>
          {restaurant.cuisine} {restaurant.price ? `• ${restaurant.price}` : ""}
        </p>
      </div>
    </div>
  );
}
import { useNavigate } from "react-router-dom";
import type { Restaurant } from "../types";

interface Props {
  restaurant: Restaurant;
}

export default function RestaurantCard({ restaurant }: Props) {
  const navigate = useNavigate();

  return (
    <div className="restaurant-card-home">
      <img
        src={restaurant.image_url}
        alt={restaurant.name}
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
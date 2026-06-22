import { useNavigate } from "react-router-dom";
import type { Restaurant } from "../types";

interface Props {
  restaurant: Restaurant | {
    id: number;
    name: string;
    cuisine: string;
    rating: number;
    price: string;
    image: string;
  };
}

export default function RestaurantCard({
  restaurant,
}: Props) {
  const navigate = useNavigate();

  // Support both field name conventions - use as any to avoid strict type errors
  const r = restaurant as any;
  const imageUrl = r.image || r.image_url;
  const cuisineCategory = r.cuisine || r.category;
  const rating = r.rating || r.avg_rating || 0;
  const price = r.price || r.price_level;

  return (
    <div className="restaurant-card-home">
      <img
        src={imageUrl}
        alt={restaurant.name}
        onClick={() =>
          navigate("/restaurant")
        }
      />

      <div className="restaurant-card-content">
        <h3>{restaurant.name}</h3>

        <span>
          ⭐ {rating}
        </span>

        <p>
          {cuisineCategory} • {price}
        </p>
      </div>
    </div>
  );
}
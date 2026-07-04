import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import "./RestaurantPage.css";
// import api from "../api/client"; // Adjust to your actual API client import

export default function RestaurantPage() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>(); 
  
  const [restaurant, setRestaurant] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Replace this with your actual API call
    const fetchRestaurant = async () => {
      try {
        setLoading(true);
        // const response = await api.get(`/restaurants/${id}`);
        // setRestaurant(response.data);
        
        // TEMPORARY MOCK DATA to test the new layout until your API is hooked up:
        setTimeout(() => {
          setRestaurant({
            name: "Sushi Nakazawa",
            avg_rating: 4.8,
            price: "$$$",
            cuisine: "Japanese",
            description: "An upscale, omakase-only sushi experience crafted by an apprentice of Jiro Ono.",
            image_url: "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=800&q=80",
            address: "123 Culinary Lane, Food City"
          });
          setLoading(false);
        }, 800);
      } catch (error) {
        console.error("Failed to fetch restaurant", error);
        setLoading(false);
      }
    };

    if (id) fetchRestaurant();
  }, [id]);

  return (
    <AppShell>
      <div className="restaurant-page">
        {loading ? (
          <div className="loading-state">Loading delicious details...</div>
        ) : !restaurant ? (
          <div className="error-state">Restaurant not found.</div>
        ) : (
          <>
            {/* HERO IMAGE */}
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
                <span>⭐ {restaurant.avg_rating}</span>
                {restaurant.price && <span>• {restaurant.price}</span>}
                {restaurant.cuisine && <span>• {restaurant.cuisine}</span>}
              </div>

              {/* Assuming you pass the tag via state or calculate it */}
              <div className="recommendation-tag">Recommended For You</div>

              <p className="restaurant-description">
                {restaurant.description || "A fantastic local spot worth checking out."}
              </p>

              {/* BUTTON GRID */}
              <div className="actions-row">
                <button className="action-btn">❤️ Like</button>
                <button className="action-btn secondary">👎 Dislike</button>
              </div>

              <button 
                className="maps-btn"
                onClick={() => window.open(`https://maps.google.com/?q=${restaurant.name} ${restaurant.address || ''}`)}
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
import { useLocation, useNavigate } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import "./VibeMatchPage.css";
import RestaurantCard from "../components/RestaurantCard";

export default function VibeMatchResultPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const recommendations = location.state?.recommendations || [];

  return (
    <AppShell>
      <div className="vibe-result-page">
        <button
          className="vibe-back-btn"
          onClick={() => navigate("/home")}
        >
          ← Back
        </button>

        {recommendations.length > 0 ? (
            <div className="vibe-results-list">
                <h2>🪄 Best Matches for you</h2>

                {recommendations.map((restaurant: any) => (
                    <RestaurantCard
                        key={restaurant.gmap_id || restaurant.id || restaurant.name}
                        restaurant={restaurant}
                        variant="list"
                    />
                ))}
            </div>
        ) : (
          <div className="vibe-empty-state">
            <h3>No matches found</h3>
            <p>Try changing your filters and searching again.</p>
          </div>
        )}
      </div>
    </AppShell>
  );
}
import "./Onboarding.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AppShell from "../layouts/AppShell";
import { vibeService } from "../api/services"; // CHANGED: Using centralized architecture
import { preloadHomeData } from "../api/home";

import { useAuth } from "../contexts/AuthContext";

const CUISINE_OPTIONS = ["Sushi", "Italian", "Dessert", "Cafe", "Burger", "Mexican", "Seafood", "Fast food"];
const VIBE_OPTIONS = ["Cozy", "Casual", "Romantic", "Trendy", "Family-friendly", "Upscale"];
const ACCESSIBILITY_OPTIONS = ["Required", "Not Required"];
const DIETARY_OPTIONS = ["Gluten Free", "Vegetarian", "Vegan", "None"];

export default function Onboarding() {
  const navigate = useNavigate();
  // Safe fallbacks to local mock attributes if user lands here without a real login session

  const { userData } = useAuth();
  const userId = userData.user_id;
  const username = userData.username || "Mock User";

  // Multi-select for cuisines and vibes
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>([]);
  const [selectedVibes, setSelectedVibes] = useState<string[]>([]);

  // Single-select for accessibility and dietary
  const [accessibility, setAccessibility] = useState("");
  const [dietary, setDietary] = useState("");

  const toggleSelection = (
    item: string,
    setList: React.Dispatch<React.SetStateAction<string[]>>,
  ) => {
    setList((prev) =>
      prev.includes(item)
              ? prev.filter((i) => i !== item)
              : [...prev, item]
          );  
  };

  const handleComplete = async () => {
    if (!userId) {
      navigate("/login", { replace: true });
      return;
    }

    const userPreferences = {
      favorite_categories: selectedCuisines,
      favorite_atmospheres: selectedVibes,
      accessibility: accessibility,
      dietary_restrictions: dietary,
    };

    try {
      // 1. Try hitting the central service wrapper mapped to your teammate's backend
      await vibeService.submitMatch(userId, userPreferences);
      console.log("Successfully saved backend preferences:", userPreferences);

    } catch (error) {
      // 2. STABILITY FALLBACK: Intercept 404/Connection errors gracefully
            console.warn("Backend offline. Simulating local onboarding preferences save...", error);
    } finally {
      // Always advance to home safely regardless of server availability status
      preloadHomeData(userId);
      navigate("/loading", {
        state: {
          nextPage: "/home",
          username: userData.username  // Propagate the username down to the home layout state
        },
        replace: true,
      });
    }
  };

  return (
    <AppShell>
      <div className="onboarding-page">
        <h1>Welcome{username ? `, ${username}` : ""}!</h1>
          <p>Please pick a few of your favorites so we can recommend the best places for you 😊</p>

        <div className="filters">
          <div className="preference-group">
            <label>🍽️ What do you love to eat?</label>
            <div className="segmented-control">
              {CUISINE_OPTIONS.map((option) => (
                <button
                  key={option}
                  className={selectedCuisines.includes(option) ? "segment active" : "segment"}
                  onClick={() => toggleSelection(option, setSelectedCuisines)}
                >
                  {option}
                </button>
              ))}
            </div>
          </div>

          <div className="preference-group">
            <label>✨ What's your usual vibe?</label>
            <div className="segmented-control">
              {VIBE_OPTIONS.map((option) => (
                <button
                  key={option}
                  className={selectedVibes.includes(option) ? "segment active" : "segment"}
                  onClick={() => toggleSelection(option, setSelectedVibes)}
                >
                  {option}
                </button>
              ))}
            </div>
          </div>

          <div className="preference-group">
            <label>♿ Accessibility</label>
            <div className="segmented-control">
              {ACCESSIBILITY_OPTIONS.map((value) => (
                <button
                  key={value}
                  className={accessibility === value ? "segment active" : "segment"}
                  onClick={() => setAccessibility(value)}
                >
                  {value}
                </button>
              ))}
            </div>
          </div>

          <div className="preference-group">
            <label>🥗 Dietary</label>
            <div className="segmented-control">
              {DIETARY_OPTIONS.map((value) => (
                <button
                  key={value}
                  className={dietary === value ? "segment active" : "segment"}
                  onClick={() => setDietary(value)}
                >
                  {value}
                </button>
              ))}
            </div>
          </div>
        </div>

        <button
          className="submit-btn"
          disabled={selectedCuisines.length === 0 && selectedVibes.length === 0}
          onClick={handleComplete}
        >
          Show Me Restaurants →
        </button>
      </div>
    </AppShell>
  );
}
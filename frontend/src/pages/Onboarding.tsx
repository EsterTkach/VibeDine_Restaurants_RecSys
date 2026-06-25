import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import AppShell from "../layouts/AppShell";

import "./Onboarding.css";

const CUISINE_OPTIONS = ["Sushi", "Italian", "Dessert", "Cafe", "Burger", "Mexican", "Seafood", "Fast food"];
const VIBE_OPTIONS = ["Cozy", "Casual", "Romantic", "Trendy", "Family-friendly", "Upscale"];
const ACCESSIBILITY_OPTIONS = ["Required", "Not Required"];
const DIETARY_OPTIONS = ["Gluten Free", "Vegetarian", "Vegan", "None"];

export default function Onboarding() {
  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state?.username;

  // Multi-select for cuisines and vibes
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>([]);
  const [selectedVibes, setSelectedVibes] = useState<string[]>([]);

  // Single-select for accessibility and dietary
  const [accessibility, setAccessibility] = useState("");
  const [dietary, setDietary] = useState("");

  const toggleSelection = (
    item: string,
    setList: React.Dispatch<React.SetStateAction<string[]>>
  ) => {
    setList((prev) =>
      prev.includes(item)
        ? prev.filter((i) => i !== item)
        : [...prev, item]
    );
  };

  const handleComplete = () => {
    const userPreferences = {
      favorite_categories: selectedCuisines,
      favorite_atmospheres: selectedVibes,
      accessibility: accessibility,
      dietary_restrictions: dietary,
    };

    console.log("Saving preferences:", userPreferences);

    // Navigates to the loading page, then bounces to home!
    navigate("/loading", {
      state: {
        nextPage: "/home",
      },
    });
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
                  className={
                    selectedCuisines.includes(option)
                      ? "segment active"
                      : "segment"
                  }
                  onClick={() =>
                    toggleSelection(option, setSelectedCuisines)
                  }
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
                  className={
                    selectedVibes.includes(option)
                      ? "segment active"
                      : "segment"
                  }
                  onClick={() =>
                    toggleSelection(option, setSelectedVibes)
                  }
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
                  className={
                    accessibility === value 
                      ? "segment active" 
                      : "segment"
                  }
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
                  className={
                    dietary === value 
                      ? "segment active" 
                      : "segment"
                  }
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